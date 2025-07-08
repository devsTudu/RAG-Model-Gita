from src.agents.embedders import myEmbedder
from utils.environmentVariablesHandler import get
from .base import PGVectorDataLoader, RobustPGVectorRetriever

PRIMARY_PGVECTOR: str = get("VECTOR_DATABASE_URL")
SECONDARY_PGVECTOR: str = get("BACKUP_VECTOR_DATABASE_URL")

PRIMARY_DB = PGVectorDataLoader(myEmbedder, SECONDARY_PGVECTOR, "gita")
SECONDARY_DB = PGVectorDataLoader(myEmbedder, PRIMARY_PGVECTOR, "gita")


Robust = RobustPGVectorRetriever(
    vectorstore=PRIMARY_DB.vector_db,
    fallback_retriever=SECONDARY_DB.get_retriever(),
    enable_fallback=True,
)
