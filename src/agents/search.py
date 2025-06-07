from src.vector_store.load_db import Robust


def search_for(query:str,n=4):
    # Robust.k = n
    result =Robust.invoke(query,fetch_k = n)
    return [data.model_dump_json() for data in result]