"""HCX chat wrapper."""
from __future__ import annotations
import time

import logging
import uuid, asyncio, json
from typing import (
    Type,
    Any,
    Dict,
    Iterator,
    AsyncIterator,
    List,
    Mapping,
    Optional
)

from langchain_core.callbacks import (
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import (
    BaseChatModel,
    agenerate_from_stream,
    generate_from_stream,
)
from langchain_core.language_models.llms import create_base_retry_decorator
from langchain_core.messages import (
    BaseMessage,
)
from langchain_core.outputs import (
    ChatGeneration, 
    ChatGenerationChunk, 
    ChatResult,
)
from langchain_core.pydantic_v1 import (
    Field, 
    root_validator,
    SecretStr
)
from langchain_core.utils import (
    get_from_dict_or_env,
    get_pydantic_field_names,
)
from langchain_core.messages import (
    AIMessageChunk,
    BaseMessage,
    BaseMessageChunk,
    ChatMessageChunk,
    FunctionMessageChunk,
    HumanMessageChunk,
    SystemMessageChunk
)

try:
    import pyhcx
    from langchain_hcxai.utils.hcxai import (
        resolve_hcx_credentials,
        convert_hcx_to_message,
        convert_message_to_hcx,
    )
except ImportError as e:
    raise ImportError(
        "HCX API not installed."
        "Please install it with `pip install hcxai`."
    ) from e

logger = logging.getLogger(__name__)


class ChatHCX(BaseChatModel):
    """`HCX` Chat large language models API.

    To use, you should have the ``HCX`` python package installed, and the
    environment variable ``HCX_API_KEY`` and ``HCX_GW_KEY`` set with your API key.

    Any parameters that are valid to be passed to the pyhcx.create call can be passed
    in, even if not explicitly saved on this class.

    Example:
        .. code-block:: python

            from langchain_community.chat_models import ChatHCX
            hcx = ChatHCX(model_name="HCX-003")
    """

    client: Any = Field(default=None, exclude=True)  #: :meta private:
    clovastudio_api_key: Optional[SecretStr] = Field(default=None)
    apigw_api_key: Optional[SecretStr] = Field(default=None)
    api_base: Optional[str] = Field(default=None)
    app_name: Optional[str] = Field(default='serviceapp')
    streaming: bool = Field(default=False)
    task_id: Optional[str] = Field(default=None)
    
    model_name: str = Field(default="HCX-003", alias="model")
    temperature: float = 0.5
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    max_tokens: Optional[int] = Field(default=100)

    chat_api: Any = Field(default=None, exclude=True)

    class Config:
        """Configuration for this pydantic object."""
        allow_population_by_field_name = True

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {
            "clovastudio_api_key": "CLOVASTUDIO_API_KEY", 
            "apigw_api_key": "APIGW_API_KEY"
            }
    
    @property
    def lc_serializable(self) -> bool:
        return True
    
    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "chat_models", "hcxai"]
    
    @property
    def _llm_type(self) -> str:
        """Return type of chat model."""
        return "hcxai-chat"

    @property
    def lc_attributes(self) -> Dict[str, Any]:
        attributes: Dict[str, Any] = {}
        if self.clovastudio_api_key:
            attributes["clovastudio_api_key"] = self.clovastudio_api_key
        if self.apigw_api_key:
            attributes["apigw_api_key"] = self.apigw_api_key
        if self.api_base:
            attributes["api_base"] = self.api_base
        return attributes
    
    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Build extra kwargs from additional params that were passed in."""
        all_required_field_names = get_pydantic_field_names(cls)
        extra = values.get("model_kwargs", {})
        for field_name in list(values):
            if field_name in extra:
                raise ValueError(f"Found {field_name} supplied twice.")
            if field_name not in all_required_field_names:
                logger.warning(
                    f"""WARNING! {field_name} is not default parameter.
                    {field_name} was transferred to model_kwargs.
                    Please confirm that {field_name} is what you intended."""
                )
                extra[field_name] = values.pop(field_name)

        invalid_model_kwargs = all_required_field_names.intersection(extra.keys())
        if invalid_model_kwargs:
            raise ValueError(
                f"Parameters {invalid_model_kwargs} should be specified explicitly. "
                f"Instead they were passed in as part of `model_kwargs` parameter."
            )

        values["model_kwargs"] = extra
        return values

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api id and python package exists in environment."""        
        api_base = get_from_dict_or_env(values, "api_base", "HCX_API_BASE")
        if (api_base == None):
            values["api_base"] = "https://clovastudio.stream.ntruss.com"

        client = pyhcx.ApiClient(resolve_hcx_credentials(**values))
        values["client"] = client
        chat_api = pyhcx.ChatApi(client)
        values["chat_api"] = chat_api

        return values

    @property
    def _model_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling HCX API."""
        normal_params = {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        return {**normal_params, **self.model_kwargs}
    
    def _get_parmas(self, stop: Optional[List[str]]) -> Dict[str, Any]:
        params = self._model_params
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop_before"] = stop

        return params
    
    def _create_chat_result(self, response: pyhcx.CreateChatCompletionResponse) -> ChatResult:
        if (hasattr(response, "status") and response.status.code != "20000"):
            raise ValueError(response)
        
        generations = []
        message = convert_hcx_to_message(response.result.message)
        generation_info = dict(finish_reason=response.result.stop_reason)
        gen = ChatGeneration(
            message=message,
            generation_info=generation_info,
        )
        generations.append(gen)
        token_usage = (response.result.input_length or 0) + (response.result.output_length or 0)
        llm_output = {
            "token_usage": token_usage,
            "model_name": self.model_name,
            "system_fingerprint": "",
        }
        return ChatResult(generations=generations, llm_output=llm_output)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = self._stream(
                messages=messages, stop=stop, run_manager=run_manager, **kwargs
            )
            return generate_from_stream(stream_iter)

        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": False}
        messages_hcx = [convert_message_to_hcx(m) for m in messages]

        api_request = pyhcx.CreateChatCompletionRequest(messages=messages_hcx, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        max_attempt = 7
        for attempt in range(max_attempt + 1):
            try:
                if self.task_id:
                    api_response = self.chat_api.create_training_chat_completion(self.app_name, self.task_id, api_request_id, api_request)
                else:
                    api_response = self.chat_api.create_chat_completion(self.app_name, self.model_name, api_request_id, api_request)
                if (hasattr(api_response, "status") and api_response.status.code == "20000"):
                    return self._create_chat_result(api_response)
            except pyhcx.ApiException as e:
                if attempt < max_attempt and e.status == 429:
                    print(f"HCX Chat Error... Try Again: {attempt + 1}/{max_attempt}")
                    print(e)
                    time.sleep(10)  
                else:
                    print(f"HCX Chat request failed after {attempt + 1} attempts")
                    raise ValueError("Exception when calling ChatApi->create_chat_completion: %s\n" % e)
    
    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.streaming:
            stream_iter = await self._astream(
                messages=messages, stop=stop, run_manager=run_manager, **kwargs
            )
            return agenerate_from_stream(stream_iter)

        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": False}
        messages_hcx = [convert_message_to_hcx(m) for m in messages]

        api_request = pyhcx.CreateChatCompletionRequest(messages=messages_hcx, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        max_attempt = 7
        for attempt in range(max_attempt + 1):
            try:
                if self.task_id:
                    api_response = await asyncio.to_thread(
                        self.chat_api.create_training_chat_completion,
                        self.app_name, self.task_id, api_request_id, api_request
                        )
                else:
                    api_response = await asyncio.to_thread(
                        self.chat_api.create_chat_completion,
                        self.app_name, self.model_name, api_request_id, api_request
                        )
                if (hasattr(api_response, "status") and api_response.status.code == "20000"):
                    return self._create_chat_result(api_response)
            except pyhcx.ApiException as e:
                if attempt < max_attempt and e.status == 429:
                    print(f"Async HCX Chat Error... Try Again: {attempt + 1}/{max_attempt}")
                    print(e)
                    await asyncio.sleep(10)
                else:
                    print(f"Async HCX Chat request failed after {attempt + 1} attempts")
                    raise ValueError("Exception when calling ChatApi->create_chat_completion: %s\n" % e)
        
    
    def _stream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[ChatGenerationChunk]:
        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": True}
        messages_hcx = [convert_message_to_hcx(m) for m in messages]

        api_request = pyhcx.CreateChatCompletionRequest(messages=messages_hcx, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        max_attempt = 7
        while max_attempt > 0:
            max_attempt -= 1
            try:
                if self.task_id:
                    api_response = self.chat_api.create_training_chat_completion_without_preload_content(
                        self.app_name, 
                        self.task_id, 
                        api_request_id, 
                        api_request, _headers={'Accept': 'text/event-stream'}
                        )
                else:
                    api_response = self.chat_api.create_chat_completion_without_preload_content(
                        self.app_name, 
                        self.model_name, 
                        api_request_id, 
                        api_request, _headers={'Accept': 'text/event-stream'}
                        )
                if (hasattr(api_response, "status") and api_response.status == 200):
                    for _line in api_response:
                        line = _parse_stream_helper(_line)
                        if line:
                            chunk = _handle_sse_line(line)
                            if chunk:
                                cg_chunk = ChatGenerationChunk(message=chunk, generation_info=None)
                                if run_manager:
                                    run_manager.on_llm_new_token(str(chunk.content), chunk=cg_chunk)
                                yield cg_chunk
                    max_attempt = 0
            except pyhcx.ApiException as e:
                if max_attempt > 0  and e.status == 429:
                    print(f"Stream HCX Chat Error... Try Again: {max_attempt}")
                    print(e)
                    time.sleep(10)  
                else:
                    print(f"Stream HCX Chat request failed after {max_attempt} attempts")
                    raise ValueError("Exception when calling ChatApi->create_chat_completion_without_preload_content: %s\n" % e)
    
    async def _astream(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[ChatGenerationChunk]:
        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": True}
        messages_hcx = [convert_message_to_hcx(m) for m in messages]

        api_request = pyhcx.CreateChatCompletionRequest(messages=messages_hcx, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        max_attempt = 7
        while max_attempt > 0:
            max_attempt -= 1
            try:
                if self.task_id:
                    api_response = await asyncio.to_thread(
                        self.chat_api.create_training_chat_completion_without_preload_content,
                        self.app_name, 
                        self.task_id, 
                        api_request_id, 
                        api_request, _headers={'Accept': 'text/event-stream'}
                    )
                else:
                    api_response = await asyncio.to_thread(
                        self.chat_api.create_chat_completion_without_preload_content,
                        self.app_name,
                        self.model_name, 
                        api_request_id, 
                        api_request, _headers={'Accept': 'text/event-stream'}
                    )
                if (hasattr(api_response, "status") and api_response.status == 200):
                    for _line in api_response:
                        line = _parse_stream_helper(_line)
                        if line:
                            chunk = _handle_sse_line(line)
                            if chunk:
                                cg_chunk = ChatGenerationChunk(message=chunk, generation_info=None)
                                if run_manager:
                                    await run_manager.on_llm_new_token(str(chunk.content), chunk=cg_chunk)
                                yield cg_chunk
                    max_attempt = 0
            except pyhcx.ApiException as e:
                if max_attempt > 0 and e.status == 429:
                    print(f"Stream HCX Chat Error... Try Again: {max_attempt}")
                    print(e)
                    time.sleep(10)  
                else:
                    print(f"Stream HCX Chat request failed after {max_attempt} attempts")
                raise ValueError("Exception when calling ChatApi->create_chat_completion_without_preload_content: %s\n" % e)


def _parse_stream_helper(line: bytes) -> Optional[str]:
    if line and line.startswith(b"data:"):
        if line.startswith(b"data: "):
            line = line[len(b"data: ") :]
        else:
            line = line[len(b"data:") :]
        if line.strip() == b"[DONE]":
            return None
        else:
            return line.decode("utf-8")
    return None

def _handle_sse_line(line: str) -> Optional[BaseMessageChunk]:
    try:
        obj = json.loads(line)
        default_chunk_class = AIMessageChunk
        delta = obj.get("message", {})
        return _convert_delta_to_message_chunk(delta, default_chunk_class)
    except Exception:
        return None

def _convert_delta_to_message_chunk(
    _dict: Mapping[str, Any], default_class: Type[BaseMessageChunk]
) -> BaseMessageChunk:
    role = _dict.get("role")
    content = _dict.get("content") or ""
    if _dict.get("function_call"):
        additional_kwargs = {"function_call": dict(_dict["function_call"])}
    else:
        additional_kwargs = {}

    if role == "user" or default_class == HumanMessageChunk:
        return HumanMessageChunk(content=content)
    elif role == "assistant" or default_class == AIMessageChunk:
        return AIMessageChunk(content=content, additional_kwargs=additional_kwargs)
    elif role == "system" or default_class == SystemMessageChunk:
        return SystemMessageChunk(content=content)
    elif role == "function" or default_class == FunctionMessageChunk:
        return FunctionMessageChunk(content=content, name=_dict["name"])
    elif role or default_class == ChatMessageChunk:
        return ChatMessageChunk(content=content, role=role)
    else:
        return default_class(content=content)
