from __future__ import annotations

import logging
from typing import Any, Iterable, List, Optional, Tuple, Union, Callable

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores.milvus import Milvus

logger = logging.getLogger(__name__)

class MMRMilvus(Milvus):
    """Add by DIDM365"""

    def __init__(
        self,
        embedding_function: Embeddings,
        collection_name: str = "LangChainCollection",
        collection_description: str = "",
        collection_properties: Optional[dict[str, Any]] = None,
        connection_args: Optional[dict[str, Any]] = None,
        consistency_level: str = "Session",
        index_params: Optional[dict] = None,
        search_params: Optional[dict] = None,
        drop_old: Optional[bool] = False,
        *,
        operation: Optional[Callable[[List[int], List[float]], List[int]]] = None,
        auto_id: bool = False,
        primary_field: str = "pk",
        text_field: str = "text",
        vector_field: str = "vector",
        metadata_field: Optional[str] = None,
        partition_key_field: Optional[str] = None,
        partition_names: Optional[list] = None,
        replica_number: int = 1,
        timeout: Optional[float] = None,
    ):
        super().__init__(
            embedding_function,
            collection_name,
            collection_description,
            collection_properties,
            connection_args,
            consistency_level,
            index_params,
            search_params,
            drop_old,
            auto_id=auto_id,
            primary_field=primary_field,
            text_field=text_field,
            vector_field=vector_field,
            metadata_field=metadata_field,
            partition_key_field=partition_key_field,
            partition_names=partition_names,
            replica_number=replica_number,
            timeout=timeout,
        )
        self.operation = operation
    
    def calc_new_ordering(self, ids: List[int], scores: List[float]) -> List[int]:
        if self.operation == None:
            return ids
        else:
            if len(ids) == len(scores):
                return self.operation(ids, scores)
            else:
                raise ValueError("Must same dimesion for ids and scores !")


    def max_marginal_relevance_search_by_vector(
        self,
        embedding: list[float],
        k: int = 4,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        param: Optional[dict] = None,
        expr: Optional[str] = None,
        timeout: Optional[int] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Perform a search and return results that are reordered by MMR.

        Args:
            embedding (str): The embedding vector being searched.
            k (int, optional): How many results to give. Defaults to 4.
            fetch_k (int, optional): Total results to select k from.
                Defaults to 20.
            lambda_mult: Number between 0 and 1 that determines the degree
                        of diversity among the results with 0 corresponding
                        to maximum diversity and 1 to minimum diversity.
                        Defaults to 0.5
            param (dict, optional): The search params for the specified index.
                Defaults to None.
            expr (str, optional): Filtering expression. Defaults to None.
            timeout (int, optional): How long to wait before timeout error.
                Defaults to None.
            kwargs: Collection.search() keyword arguments.

        Returns:
            List[Document]: Document results for search.
        """
        if self.col is None:
            logger.debug("No existing collection to search.")
            return []

        if param is None:
            param = self.search_params

        # Determine result metadata fields.
        output_fields = self.fields[:]
        output_fields.remove(self._vector_field)

        # Perform the search.
        res = self.col.search(
            data=[embedding],
            anns_field=self._vector_field,
            param=param,
            limit=fetch_k,
            expr=expr,
            output_fields=output_fields,
            timeout=timeout,
            **kwargs,
        )
        # Organize results.
        ids = []
        scores = []
        for result in res[0]:
            scores.append(result.score)
            ids.append(result.id)

        new_ordering = self.calc_new_ordering(ids, scores)

        qry = self.col.query(
            expr=f"{self._primary_field} in {new_ordering}",
            output_fields=output_fields,
            timeout=timeout,
        )
        documents = []
        for result in qry:
            data = {x: result.get(x) for x in output_fields}
            doc = self._parse_document(data)
            documents.append(doc)

        return documents