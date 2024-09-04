"""Callback Handler that prints to std out."""
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, TypeVar, Union, Iterable, Tuple
from uuid import UUID

from tenacity import RetryCallState

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk, LLMResult

try:
    import aiohttp
    import asyncio
except ImportError:
    raise ImportError(
        "To use the aiohttp callback manager you need to have the "
        "`aiohttp` python package installed. Please install it with"
        " `pip3 install aiohttp`"
    )

def _flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Iterable[Tuple[str, Any]]:
    for key, value in nested_dict.items():
        new_key = parent_key + sep + key if parent_key else key
        if isinstance(value, dict):
            yield from _flatten_dict(value, new_key, sep)
        else:
            yield new_key, value

def flatten_dict(
    nested_dict: Dict[str, Any], parent_key: str = "", sep: str = "_"
) -> Dict[str, Any]:
    flat_dict = {k: v for k, v in _flatten_dict(nested_dict, parent_key, sep)}
    # for key, value in nested_dict.items():
    #     if isinstance(value, dict):
    #         yield key, str(value)
    return flat_dict

def transformed_messages(messages: List[BaseMessage]):
    return [(d.dict()) for d in messages]

class HCXCallbackHandler(AsyncCallbackHandler):
    """Callback Handler that tracks HCX info."""
    
    _project_name: str = "Callback"
    _project_version: str = "1.0.0"
    _url = 'https://elsa-col.ncloud.com/_store'
    _headers = {
        'Content-Type': 'application/json',
    }
    _resource: dict = None
    verbose: bool = False
    log_source:str = ""

    def __init__(
        self,
        project_name: str,
        project_version: str = None,
        verbose: bool = False,
        resource: Dict[str, Any] = None,
    ) -> None:
        super().__init__()
        self._project_name = project_name or "Callback"
        self._project_version = project_version or "1.0.0"
        self._resource = resource
        self.verbose = verbose or False

    async def add_event(self, name: str, resp: Dict[str, Any]) -> bool:
        data = {
            "projectName": self._project_name,
            "projectVersion": self._project_version,
            "body": str(resp),
            "logLevel": "DEBUG",
            "logType": name,
            "logSource": self.log_source
        }
        if self._resource:
            data = {**self._resource, **data}
        await self.send_log(data)

    async def send_log(self, data: dict) -> bool:
        # print(data)
        async with aiohttp.ClientSession() as session:
            async with session.post(self._url, headers=self._headers, json=data) as response:
                if response.status == 200:
                    return True
                else:
                    response_json = await response.json()
                    raise Exception(f"Error sending log: {response.status} - {response_json}")
                return False

    @property
    async def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return self.verbose

    async def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM starts running."""
        resp: Dict[str, Any] = flatten_dict(serialized)
        resp.update({"prompts": prompts})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_llm_start", resp)

    async def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a chat model starts running."""
        resp: Dict[str, Any] = flatten_dict(serialized)
        resp.update({"messages": str([transformed_messages(mlist) for mlist in messages])})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_chat_model_start", resp)

    async def on_llm_new_token(
        self,
        token: str,
        *,
        chunk: Optional[Union[GenerationChunk, ChatGenerationChunk]] = None,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        resp: Dict[str, Any] = {"token": token}
        resp.update({"chunk": chunk.dict()})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_llm_new_token", resp)

    async def on_llm_end(
        self,
        response: LLMResult,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM ends running."""
        resp: Dict[str, Any] = flatten_dict(response.dict())
        resp['generations'] = str(resp['generations'])
        resp['run'] = str(resp['run'])
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_llm_end", resp)

    async def on_llm_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when LLM errors.
        Args:
            error (BaseException): The error that occurred.
            kwargs (Any): Additional keyword arguments.
                - response (LLMResult): The response which was generated before
                    the error occurred.
        """
        resp: Dict[str, Any] = {"error": error.args}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_llm_error", resp)

    async def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""
        resp: Dict[str, Any] = flatten_dict(serialized)
        resp.update({"inputs": str(flatten_dict(inputs))})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_chain_start", resp)

    async def on_chain_end(
        self,
        outputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain ends running."""
        resp: Dict[str, Any] = flatten_dict(outputs)
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_chain_end", resp)

    async def on_chain_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when chain errors."""
        resp: Dict[str, Any] = {"error": error.args}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_chain_error", resp)

    async def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when tool starts running."""
        resp: Dict[str, Any] = flatten_dict(serialized)
        resp.update({"input_str": input_str})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_tool_start", resp)

    async def on_tool_end(
        self,
        output: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when tool ends running."""
        resp: Dict[str, Any] = {"output": output}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_tool_end", resp)

    async def on_tool_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run when tool errors."""
        resp: Dict[str, Any] = {"error": error.args}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_tool_error", resp)

    async def on_text(
        self,
        text: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on arbitrary text."""
        resp: Dict[str, Any] = {"text": text}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_text", resp)

    async def on_retry(
        self,
        retry_state: RetryCallState,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run on a retry event."""
        resp: Dict[str, Any] = {}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_retry", resp)

    async def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on agent action."""
        resp: Dict[str, Any] = flatten_dict(action.dict())
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_agent_action", resp)

    async def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on agent end."""
        resp: Dict[str, Any] = flatten_dict(finish.dict())
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_agent_finish", resp)

    async def on_retriever_start(
        self,
        serialized: Dict[str, Any],
        query: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever start."""
        resp: Dict[str, Any] = flatten_dict(serialized)
        resp.update({"query": query})
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_retriever_start", resp)

    async def on_retriever_end(
        self,
        documents: Sequence[Document],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever end."""
        resp: Dict[str, Any] = {"documents": [transformed_messages(d) for d in documents]}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_retriever_end", resp)

    async def on_retriever_error(
        self,
        error: BaseException,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        tags: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> None:
        """Run on retriever error."""
        resp: Dict[str, Any] = {"error": error.args}
        if parent_run_id is None:
            self.log_source = str(run_id)
        await self.add_event("on_retriever_error", resp)

    # async def __del__(self):
    #     self.step = 0

    async def __copy__(self) -> "HCXCallbackHandler":
        """Return a copy of the callback handler."""
        return self

    async def __deepcopy__(self, memo: Any) -> "HCXCallbackHandler":
        """Return a deep copy of the callback handler."""
        return self
