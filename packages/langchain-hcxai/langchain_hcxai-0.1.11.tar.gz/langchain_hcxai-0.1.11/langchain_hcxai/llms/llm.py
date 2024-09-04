from __future__ import annotations

import logging
import uuid, asyncio
from typing import (
    Any,
    AsyncIterator,
    Dict,
    Iterator,
    List,
    Optional,
)

from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import Generation, GenerationChunk, LLMResult
from langchain_core.pydantic_v1 import Field, root_validator, SecretStr
from langchain_core.utils import get_from_dict_or_env, get_pydantic_field_names

try:
    import pyhcx
    from langchain_hcxai.utils.hcxai import (
        resolve_hcx_credentials,
    )
except ImportError as e:
    raise ImportError(
        "HCX API not installed."
        "Please install it with `pip install hcxai`."
    ) from e

logger = logging.getLogger(__name__)


class llmHCX(BaseLLM):
    """Base HCX large language model class."""

    client: Any = Field(default=None, exclude=True)  #: :meta private:
    clovastudio_api_key: Optional[SecretStr] = Field(default=None)
    apigw_api_key: Optional[SecretStr] = Field(default=None)
    api_base: Optional[str] = Field(default=None)

    streaming: bool = False
    
    app_name: str = Field(default="serviceapp")
    model: str = Field(default="LK-D2", alias="model")
    temperature: float = 0.5
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    max_tokens: Optional[int] = Field(default=100)

    completions_api: Any = Field(default=None, exclude=True)

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {
            "clovastudio_api_key": "CLOVASTUDIO_API_KEY", 
            "apigw_api_key": "APIGW_API_KEY"
            }

    @classmethod
    def get_lc_namespace(cls) -> List[str]:
        """Get the namespace of the langchain object."""
        return ["langchain", "llms", "hcxai"]
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm model."""
        return "hcxai"

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

    @classmethod
    def is_lc_serializable(cls) -> bool:
        return True

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
            values["api_base"] = "https://clovastudio.apigw.ntruss.com"

        client = pyhcx.ApiClient(resolve_hcx_credentials(**values))
        values["client"] = client
        completions_api = pyhcx.CompletionsApi(client)
        values["completions_api"] = completions_api

        return values

    @property
    def _model_params(self) -> Dict[str, Any]:
        """Get the default parameters for calling HCX API."""
        normal_params = {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        return {**normal_params, **self.model_kwargs}

    def _get_parmas(self, stop: Optional[List[str]]) -> Dict[str, Any]:
        params = self._model_params
        if stop is not None:
            if "stop" in params:
                raise ValueError("`stop` found in both the input and default params.")
            params["stop_before"] = stop or []

        return params
    
    def create_completion_result(self, response: pyhcx.CreateCompletionResponse) -> LLMResult:
        if (hasattr(response, "status") and response.status.code != "20000"):
            raise ValueError(response)
        
        generations = []
        text = response.result.text
        generation_info = dict(finish_reason=response.result.stop_reason)
        gen = Generation(
            text=text,
            generation_info=generation_info,
        )
        generations.append([gen])
        token_usage = (response.result.input_tokens or 0) + (response.result.output_tokens or 0)
        llm_output = {
            "token_usage": token_usage,
            "model": self.model,
        }

        return LLMResult(generations=generations, llm_output=llm_output)

    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": False}
        text = prompts[0]

        api_request = pyhcx.CreateCompletionRequest(text=text, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        try:
            api_response = self.completions_api.create_completion(self.app_name, self.model, api_request_id, api_request)
        except pyhcx.ApiException as e:
            raise ValueError("Exception when calling completions_api->create_completion: %s\n" % e)
        
        return self.create_completion_result(api_response)

    async def _agenerate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> LLMResult:
        params = self._get_parmas(stop)
        params = {**params, **kwargs, "stream": False}
        text = prompts[0]

        api_request = pyhcx.CreateCompletionRequest(text=text, **params)
        api_request_id = str(uuid.uuid4())
        api_response = None
        try:
            api_response = await asyncio.to_thread(
                self.completions_api.create_completion,
                self.app_name, self.model, api_request_id, api_request
                )
        except pyhcx.ApiException as e:
            raise ValueError("Exception when calling completions_api->create_completion: %s\n" % e)
        
        return self.create_completion_result(api_response)

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        raise NotImplementedError("_stream is not supported for HCX API")

    async def _astream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> AsyncIterator[GenerationChunk]:
        raise NotImplementedError("_stream is not supported for HCX API")
