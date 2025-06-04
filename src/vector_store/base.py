from abc import ABC, abstractmethod
from typing import List, Any
from langchain_core.documents import Document


class BaseDataLoader(ABC):
    """Abstract base class for loading documents into the database."""

    @abstractmethod
    def load_documents(self, list_docs:list[Document]):
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
