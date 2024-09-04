import logging
import os
from typing import (
    Any,
    Dict,
    Optional,
)

from langchain_core.chat_sessions import ChatSession
from langchain_core.messages import (
    AIMessage,
    BaseMessage,
    ChatMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_core.pydantic_v1 import SecretStr

import pyhcx

HCX_MODELS: Dict[str, int] = {
    "HCX-DASH-001": 4096,
    "HCX-003": 4096,
}

CHAT_MODELS = {
    **HCX_MODELS,
}

DEFAULT_HCXAI_API_TYPE = "clovastudio_ai"
DEFAULT_HCXAI_API_BASE = "https://clovastudio.stream.ntruss.com/serviceapp/v1"

MISSING_API_KEY_ERROR_MESSAGE = """No API key found for HCX AI.
Please set either the APIGW_API_KEY and CLOVASTUDIO_API_KEY environment variable prior to initialization.
API keys can be found or created at \
https://www.ncloud.com/mypage/manage/authkey
"""

logger = logging.getLogger(__name__)

def get_from_param_or_env(
    key: str,
    param: Optional[str] = None,
    env_key: Optional[str] = None,
    default: Optional[str] = None,
) -> str:
    """Get a value from a param or an environment variable."""
    if param is not None:
        return param
    elif env_key and env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )

def resolve_hcx_credentials(
    apigw_api_key: Optional[SecretStr] = None,
    clovastudio_api_key: Optional[SecretStr] = None,
    api_base: Optional[str] = None,
    **kwargs: Any
) -> pyhcx.Configuration:
    configuration = pyhcx.Configuration(
        host = api_base or "https://clovastudio.stream.ntruss.com/serviceapp/v1"
    )
    configuration.api_key["ApigwApiKey"] = get_from_param_or_env("ApigwApiKey", apigw_api_key.get_secret_value(), "APIGW_API_KEY", "")
    configuration.api_key["ClovastudioApiKey"] = get_from_param_or_env("ClovastudioApiKey", clovastudio_api_key.get_secret_value(), "CLOVASTUDIO_API_KEY", "")
    return configuration

def convert_hcx_to_message(message: pyhcx.ChatCompletionMessage) -> BaseMessage:
    """Convert a HCX to a LangChain message."""
    # print("rsp.HCX:" + str(message))

    role = message.role
    content = message.content or ""
    additional_kwargs = message.model_dump(exclude=["role","content"])

    return ChatMessage(content=content, role=role, additional_kwargs=additional_kwargs)


def convert_message_to_hcx(message: BaseMessage) -> pyhcx.ChatCompletionMessage:
    """Convert a LangChain message to a HCX."""
    # print("req.HCX:" + str(message))

    if(hasattr(message, "role")):
        return pyhcx.ChatCompletionMessage(role=message.role, content=message.content)
    elif isinstance(message, HumanMessage):
        return pyhcx.ChatCompletionMessage(role="user", content=message.content)
    elif isinstance(message, AIMessage):
        return pyhcx.ChatCompletionMessage(role="assistant", content=message.content)
    elif isinstance(message, SystemMessage):
        return pyhcx.ChatCompletionMessage(role="system", content=message.content)
    else:
        raise TypeError(f"Got unknown type {message}")
