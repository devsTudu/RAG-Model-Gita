from abc import ABC, abstractmethod
from typing import List, Any, Optional

from langchain_core.retrievers import BaseRetriever
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.documents import Document
from langchain_postgres import PGVector

from tenacity import retry, wait_exponential, stop_after_attempt, Retrying

from utils.logger import get_logger

# Configure logging
logger = get_logger(__name__)


class BaseDataLoader(ABC):
    """Abstract base class for loading documents into the database."""

    @abstractmethod
    def load_documents(self, list_docs: list[Document]):
        """Load and preprocess documents from the list."""
        pass

    @abstractmethod
    def add_to_database(self, document: Document) -> None:
        """Add processed document to the vector database."""
        pass

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        """Retrieve top_k relevant documents for a query."""
        pass


class PGVectorDataLoader(BaseDataLoader):
    def __init__(self, embedder, db_url: str, tablename="gita"):

        if db_url is None:
            raise ValueError("DATABASE_URL environment variable is not set.")
        self.vector_db = PGVector(
            embedder, collection_name=tablename, connection=db_url, use_jsonb=True
        )

    def load_documents(self, list_docs: List[Document]):
        self.vector_db.add_documents(list_docs)

    def add_to_database(self, document: Document) -> None:
        self.vector_db.add_documents([document])

    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        return self.vector_db.similarity_search(query, top_k)

    def get_retriever(self):
        return self.vector_db.as_retriever(search_type="mmr", search_kwargs={"k": 6})


class RobustPGVectorRetriever(BaseRetriever):
    """
    A robust retriever class for PGVector databases in LangChain, incorporating
    error handling, retry mechanisms, and a fallback strategy.
    """

    vectorstore: Any  # This will be your PGVector instance
    k: int = 4
    search_type: str = "similarity"  # "similarity", "mmr", "similarity_score_threshold"
    score_threshold: Optional[float] = None  # Only for "similarity_score_threshold"
    fetch_k: Optional[int] = None  # For MMR, number of initial documents to fetch
    lambda_mult: Optional[float] = None  # For MMR, diversity score

    # Retry configuration
    max_retries: int = 3
    initial_backoff: float = 1.0  # seconds
    max_backoff: float = 10.0  # seconds

    # Fallback mechanism (optional)
    fallback_retriever: Optional[BaseRetriever] = None
    enable_fallback: bool = False

    class Config:
        """Configuration for this pydantic object."""

        arbitrary_types_allowed = True

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (
            self.search_type == "similarity_score_threshold"
            and self.score_threshold is None
        ):
            raise ValueError(
                "score_threshold must be provided for 'similarity_score_threshold' search_type."
            )
        if self.search_type == "mmr" and (
            self.fetch_k is None or self.lambda_mult is None
        ):
            logger.warning(
                "For 'mmr' search_type, 'fetch_k' and 'lambda_mult' are recommended for optimal performance."
            )

    @retry(
        wait=wait_exponential(multiplier=1, min=initial_backoff, max=max_backoff),
        stop=stop_after_attempt(max_retries),
        reraise=True,  # Re-raise the last exception if all retries fail
        before_sleep=lambda retry_state: logger.warning(
            f"Retrying PGVector search... Attempt {retry_state.attempt_number}/{self.max_retries} "
            f"after {retry_state.idle_for:.2f}s of inactivity. "
            f"Last exception: {retry_state.outcome}."
        ),
    )
    def _perform_pgvector_search(self, query: str) -> List[Document]:
        """
        Internal method to perform the actual PGVector search with retries.
        """
        logger.info(
            f"Attempting PGVector search with type: {self.search_type} for query: '{query}'"
        )
        try:
            if self.search_type == "similarity":
                docs = self.vectorstore.similarity_search(query, k=self.k)
            elif self.search_type == "mmr":
                docs = self.vectorstore.max_marginal_relevance_search(
                    query, k=self.k, fetch_k=self.fetch_k, lambda_mult=self.lambda_mult
                )
            elif self.search_type == "similarity_score_threshold":
                docs_with_scores = self.vectorstore.similarity_search_with_score(
                    query, k=self.k
                )
                docs = [
                    doc
                    for doc, score in docs_with_scores
                    if score >= self.score_threshold
                ]
            else:
                raise ValueError(f"Unsupported search_type: {self.search_type}")
            return docs
        except Exception as e:
            logger.error(f"PGVector search failed with error: {e}")
            raise LookupError(f"PGVector search failed: {e}") from e

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """
        Get relevant documents from the PGVector database,
        with robustness measures.
        """
        logger.info(f"Retrieving documents for query: '{query}'")
        retrieved_docs = []

        try:
            retrieved_docs = self._perform_pgvector_search(query)
            logger.info(
                f"Successfully retrieved {len(retrieved_docs)} documents from PGVector."
            )
            return retrieved_docs
        except LookupError as e:
            logger.error(
                f"PGVector search failed after multiple retries for query '{query}': {e}"
            )
            if self.enable_fallback and self.fallback_retriever:
                logger.warning(
                    f"Falling back to alternative retriever for query: '{query}'"
                )
                try:
                    fallback_docs = self.fallback_retriever.get_relevant_documents(
                        query, run_manager=run_manager
                    )
                    logger.info(
                        f"Successfully retrieved {len(fallback_docs)} documents from fallback retriever."
                    )
                    return fallback_docs
                except Exception as fe:
                    logger.error(
                        f"Fallback retriever also failed for query '{query}': {fe}"
                    )
                    raise RuntimeError(
                        f"Both primary and fallback retrievers failed for query: '{query}'"
                    ) from fe
            else:
                logger.error(
                    f"No fallback retriever configured or enabled. Raising original error."
                )
                raise RuntimeError(
                    f"Failed to retrieve documents from PGVector after retries: {e}"
                ) from e
        except Exception as e:
            logger.error(
                f"An unexpected error occurred during document retrieval for query '{query}': {e}"
            )
            raise RuntimeError(
                f"An unexpected error occurred during document retrieval: {e}"
            ) from e
