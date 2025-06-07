from src.vector_store.load_db import Robust
from langchain_core.documents import Document


def convert_to_string(doc:Document):
  resp = f"Reference {doc.metadata['Reference']}"
  url = "/".join(doc.metadata['Reference'].split(":"))
  resp += f" [link](https://vedabase.io/en/library/bg/{url}) \n"
  resp += f" {doc.metadata['Translation']} \n {doc.page_content.replace('"','')}"
  return resp

def search_for(query:str,n=4):
    # Robust.k = n
    result =Robust.invoke(query,fetch_k = n)
    if not result:
        return "No results found"
    return "\n\n".join([convert_to_string(doc) for doc in result])