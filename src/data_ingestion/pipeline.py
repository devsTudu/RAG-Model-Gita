from utils.file_handler import list_of_files,get_project_root
from src.data_ingestion.parsers import process_md_adv
from langchain_core.documents import Document

data_source = get_project_root().joinpath("data", "raw", "en") 
files = list_of_files(data_source,'.md',['README','SUMMARY'])
docs_dict:list[dict] = []
for file in files:
    headings = ['Translation','Purport']
    docs_dict.append(process_md_adv(file,headings))
    

docs_text:list[str] = []
for doc in docs_dict:
    if "content" in doc.keys():
        text = doc['content']
    else:
        text = f"{doc['Reference']} mentions {doc['Translation']} and it explains in purport as this {doc['Purport']}"
    docs_text.append(text)

def get_docs():
    
    docs_doc:list[Document] = []
    for doc in docs_dict:
        content:str =  f"{doc['Translation']} is spoken and it can be understood using {doc['Purport']}"
        metadata:dict = {key: value for key, value in doc.items() if key != "Purport"}
        metadata['Chapter'],metadata['Verse'] = metadata['Reference'].split(":")
        docs_doc.append(Document(page_content=content,
                                metadata=metadata
                                ))
        
    return docs_doc


def split_docs(docs: list[Document]) -> list[Document]:
    """
    Splits the content of each document into multiple documents based on the "\n\n" delimiter.

    Args:
        docs: A list of Document objects.

    Returns:
        A list of new Document objects after splitting.
    """
    split_docs_list = []
    for doc in docs:
        content = doc.page_content
        parts = content.split("\n\n")
        for part in parts:
            if part.strip():  # Avoid creating empty documents
                split_docs_list.append(Document(page_content=part, metadata=doc.metadata))
    return split_docs_list
