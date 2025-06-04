from langchain_postgres import PGVector
from langchain_core.documents import Document
from typing import Any, List

from src.agents.embedders import myEmbedder
from utils.getsecret import get
from .base import BaseDataLoader

NEON_PGVECTOR :str = get("DATABASE_URL")
SUPABASE_PGVECTOR :str = get("SUPABASE_DB_URL")

class PGVectorDataLoader(BaseDataLoader):
    def __init__(self,
                 db_url: str = NEON_PGVECTOR,
                 tablename="gita"):
        
        if db_url is None:
            raise ValueError("DATABASE_URL environment variable is not set.")
        self.vector_db = PGVector(
            myEmbedder,
            collection_name=tablename,
            connection= db_url,
            use_jsonb=True
        )
        
    def load_documents(self, list_docs: List[Document]):
        self.vector_db.add_documents(list_docs)
             
    def add_to_database(self, document: Document) -> None:
        self.vector_db.add_documents([document])   

    def retrieve(self, query: str, top_k: int = 5) -> List[Any]:
        return self.vector_db.similarity_search(query,top_k)

    def get_retriever(self):
        return self.vector_db.as_retriever(search_type='mmr',
                                           search_kwargs={"k": 6}
                                           )


Neon_DB = PGVectorDataLoader(NEON_PGVECTOR,"gita")
Supabase_DB = PGVectorDataLoader(SUPABASE_PGVECTOR,"gita")

