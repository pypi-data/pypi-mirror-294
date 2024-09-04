from __future__ import annotations

import logging
from functools import lru_cache
import uuid, asyncio
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

from langchain_core.embeddings import Embeddings
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator, SecretStr
from langchain_core.utils import get_from_dict_or_env, get_pydantic_field_names
import time

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


class HCXEmbeddings(BaseModel, Embeddings):
    """HCX embedding models.

    To use, you should have the ``HCX`` python package installed, and the
    environment variable ``HCX_API_KEY`` and ``HCX_GW_KEY`` set with your API key or pass it
    as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_community.embeddings import HCXEmbeddings
            HCX = HCXEmbeddings(clovastudio_api_key="my-api-key", apigw_api_key="my-gw-key", api_base="my-api-base")

    In order to use the library with Microsoft Azure endpoints, you need to set
    the HCX_API_BASE, HCX_API_KEY and HCX_API_VERSION
    In addition, the deployment name must be passed as the model parameter.

    Example:
        .. code-block:: python

            import os

            os.environ["CLOVASTUDIO_API_KEY"] = "your hcx api key"
            os.environ["APIGW_API_KEY"] = "your hcx gateway key"

            from langchain_community.embeddings.hcxai import HCXEmbeddings
            embeddings = HCXEmbeddings(
                model="your-embeddings-model-name",
                api_base="https://clovastudio.apigw.ntruss.com/testapp/v1",
            )
            text = "This is a test query."
            query_result = embeddings.embed_query(text)

    """
    # client params
    apigw_api_key: SecretStr = Field(default=None)
    clovastudio_api_key: SecretStr = Field(default=None)
    api_base: str = "https://clovastudio.apigw.ntruss.com"
    client: Any = Field(default=None, exclude=True)  #: :meta private:

    app_name: str = "serviceapp"
    # Embedding params
    model: str = "clir-emb-dolphin"
    """Model name to use."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Holds any model parameters valid for `create` call not explicitly specified."""

    embedding_api: Any = Field(default=None, exclude=True)
    app_id: str = Field(default=None)
    

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api id and python package exists in environment."""
        app_id = get_from_dict_or_env(values, "app_id", "HCX_APP_ID")
        if (app_id == None):
            raise ValueError("app_id is None")
        else:
            values["app_id"] = app_id
        
        api_base = get_from_dict_or_env(values, "api_base", "HCX_API_BASE")
        if (api_base == None):
            values["app_id"] = "https://clovastudio.apigw.ntruss.com"

        client = pyhcx.ApiClient(resolve_hcx_credentials(**values))
        values["client"] = client
        embedding_api = pyhcx.EmbeddingsApi(client)
        values["embedding_api"] = embedding_api

        return values


    def embed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        results: List[List[List[float]]] = [[] for _ in range(len(texts))]
        for i, text in enumerate(texts):
            response = self.embed_query(text)
            if isinstance(response, List):
                results[i] = response

        return results

    async def aembed_documents(
        self, texts: List[str], chunk_size: Optional[int] = 0
    ) -> List[List[float]]:
        results: List[List[List[float]]] = [[] for _ in range(len(texts))]
        for i, text in enumerate(texts):
            response = await self.aembed_query(text)
            if isinstance(response, List):
                results[i] = response
        
        return results

    def embed_query(self, text: str) -> List[float]:
        api_request_id = str(uuid.uuid4())
        api_request = pyhcx.CreateEmbeddingRequest(text=text)
        api_response = None
        max_attempt = 7
        for attempt in range(max_attempt + 1): 
            try: 
                api_response = self.embedding_api.create_embedding(self.app_name, self.model, self.app_id, api_request_id, api_request)
                if (hasattr(api_response, "status") and api_response.status.code == "20000"):
                    return api_response.result.embedding
            except Exception as e:
                if attempt < max_attempt and e.status == 429:
                    print(f"HCX Embedding Error... Try Again: {attempt + 1}/{max_attempt}")
                    print(e)
                    time.sleep(10)  
                else:
                    print(f"Embedding request failed after {attempt + 1} attempts")
                    raise ValueError(api_response)

    async def aembed_query(self, text: str) -> List[float]:
        api_request_id = str(uuid.uuid4())
        api_request = pyhcx.CreateEmbeddingRequest(text=text)
        api_response = None
        max_attempt = 7
        for attempt in range(max_attempt + 1):
            try: 
                api_response = await asyncio.to_thread(
                    self.embedding_api.create_embedding,
                    self.app_name, self.model, self.app_id, api_request_id, api_request
                    )
                if (hasattr(api_response, "status") and api_response.status.code == "20000"):
                    return api_response.result.embedding
            except pyhcx.ApiException as e:
                if attempt < max_attempt and e.status == 429:
                    print(f"Async HCX Embedding Error... Try Again: {attempt + 1}/{max_attempt}")
                    print(e)
                    await asyncio.sleep(10)
                else:
                    print(f"Embedding request failed after {attempt + 1} attempts")
                    raise ValueError(api_response)