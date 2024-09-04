import copy
import logging
import uuid
import itertools

from typing import (Any, Dict, List, Optional, Iterable)

from langchain_core.documents import Document
from langchain_core.pydantic_v1 import BaseModel, Field, root_validator, SecretStr
from langchain_core.utils import get_from_dict_or_env, get_pydantic_field_names

try:
    import pyhcx
    from langchain_hcxai.utils.hcxai import (
        resolve_hcx_credentials,
    )
except ImportError as e:
    raise ImportError(
        "HCX API not installed."
        "Please install it with `pip install pyhcx`."
    ) from e

logger = logging.getLogger(__name__)

class HCXTextSplitter(BaseModel):
    """HCX splitter.

    To use, you should have the ``HCX`` python package installed, and the
    environment variable ``HCX_API_KEY`` and ``HCX_GW_KEY`` set with your API key or pass it
    as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from langchain_hcxai.vectorstore.text_splitter import HCXTextSplitter
            splitter = HCXTextSplitter(clovastudio_api_key="my-api-key", apigw_api_key="my-gw-key", api_base="my-api-base")

    In order to use the library with Microsoft Azure endpoints, you need to set
    the HCX_API_BASE, HCX_API_KEY and HCX_API_VERSION
    In addition, the deployment name must be passed as the model parameter.

    Example:
        .. code-block:: python

            import os

            os.environ["CLOVASTUDIO_API_KEY"] = "your hcx api key"
            os.environ["APIGW_API_KEY"] = "your hcx gateway key"

            from langchain_community.embeddings.hcxai import HCXEmbeddings
            splitter = HCXTextSplitter(
                model="your-embeddings-model-name",
                api_base="https://clovastudio.apigw.ntruss.com",
            )
            text = "This is a test query.This is a test query.This is a test query.This is a test query.This is a test query."
            splitte_result = splitter.split_text(text)

    """
    # client params
    apigw_api_key: SecretStr = Field(default=None)
    clovastudio_api_key: SecretStr = Field(default=None)
    api_base: str = "https://clovastudio.apigw.ntruss.com"
    client: Any = Field(default=None, exclude=True)  #: :meta private:

    app_name: str = "serviceapp"

    segmentation_api: Any = Field(default=None, exclude=True)
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
            values["api_base"] = "https://clovastudio.apigw.ntruss.com"

        client = pyhcx.ApiClient(resolve_hcx_credentials(**values))
        values["client"] = client
        segmentation_api = pyhcx.SegmentationApi(client)
        values["segmentation_api"] = segmentation_api

        return values

    def split_text(
        self,
        text: str,
        *,
        alpha: float = 0.0,
        segCnt: int = -1,
        postProcess:bool = False,
        postProcessMaxSize: int = 1000,
        postProcessMinSize:int = 300
    ) -> List[str]:
        api_request_id = str(uuid.uuid4())
        api_request = pyhcx.CreateSegmentationRequest(text=text, alpha=alpha, segCnt=segCnt, postProcess=postProcess, postProcessMaxSize=postProcessMaxSize, postProcessMinSize=postProcessMinSize)
        api_response = self.segmentation_api.create_segmentation(self.app_name, self.app_id, api_request_id, api_request)
        if (hasattr(api_response, "status") and api_response.status.code == "20000"):
            flat_list = list(itertools.chain.from_iterable(api_response.result.topic_seg))
            return flat_list
        else:
            raise ValueError(api_response)
    
    def create_documents(
        self, texts: List[str], metadatas: Optional[List[dict]] = None
    ) -> List[Document]:
        """Create documents from a list of texts."""
        _metadatas = metadatas or [{}] * len(texts)
        documents = []
        for i, text in enumerate(texts):
            for chunk in self.split_text(text):
                metadata = copy.deepcopy(_metadatas[i])
                new_doc = Document(page_content=chunk, metadata=metadata)
                documents.append(new_doc)
        return documents

    def split_documents(self, documents: Iterable[Document]) -> List[Document]:
        """Split documents."""
        texts, metadatas = [], []
        for doc in documents:
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)
        return self.create_documents(texts, metadatas=metadatas)