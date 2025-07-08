from src.vector_store.load_db import Robust
from langchain_core.documents import Document


def convert_to_string(doc: Document):
    url = "/".join(doc.metadata["Reference"].split(":"))
    content = doc.page_content.replace('"', "")
    resp = content
    resp += f"\n\n"
    resp += f"{doc.metadata['Reference']} _{doc.metadata['Translation']}_\n"
    resp += f" [Chapter {doc.metadata['Chapter']} Verse {doc.metadata['Verse']}](https://vedabase.io/en/library/bg/{url}) \n"
    return resp


def search_for(query: str, n=4):
    # Robust.k = n
    result = Robust.invoke(query, fetch_k=n)
    if not result:
        return "No results found"
    resp = "Here is what I found for your query:\n"
    for i, doc in enumerate(result):
        resp += f"\n\n({i+1})  {convert_to_string(doc)}"
    return resp
