from langchain_postgres import PGVector
from langchain_core.documents import Document
from typing import Any, List

from src.agents.embedders import myEmbedder
from utils.getsecret import get
from .base import PGVectorDataLoader, RobustPGVectorRetriever

NEON_PGVECTOR :str = get("DATABASE_URL")
SUPABASE_PGVECTOR :str = get("SUPABASE_DB_URL")

Neon_DB = PGVectorDataLoader(myEmbedder,NEON_PGVECTOR,"gita")
Supabase_DB = PGVectorDataLoader(myEmbedder,SUPABASE_PGVECTOR,"gita")


Robust = RobustPGVectorRetriever(vectorstore=Supabase_DB.vector_db,
                                 fallback_retriever=Neon_DB.get_retriever(),
                                 enable_fallback=True)
