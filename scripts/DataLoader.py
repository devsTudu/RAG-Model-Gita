from src.vector_store.load_db import PRIMARY_DB, SECONDARY_DB
from src.data_ingestion.pipeline import getDocs, split_docs


def load():
    """Store the Vector Data into the connected Databases"""

    final_docs = split_docs(getDocs())
    PRIMARY_DB.load_documents(final_docs)
    SECONDARY_DB.load_documents(final_docs)
