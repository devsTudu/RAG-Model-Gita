from langchain_core.documents import Document

from utils.file_handler import list_of_files, get_project_root
from src.data_ingestion.parsers import process_md_adv

data_source = get_project_root().joinpath("data", "raw", "en")


def docs_as_dict():
    """
    Return the document after parseing important infomations
    """
    files = list_of_files(data_source, ".md", ["README", "SUMMARY"])
    docs_dict: list[dict] = []
    for file in files:
        headings = ["Translation", "Purport"]
        docs_dict.append(process_md_adv(file, headings))
    return docs_dict


def docs_in_text() -> list[str]:
    """Get a string representation of all the files"""

    docs_text: list[str] = []
    for doc in docs_as_dict():
        if "content" in doc.keys():
            Texts = doc["content"]
        else:
            Texts = f"{doc['Reference']} mentions {doc['Translation']}"
            Texts += f"and it explains in purport as this {doc['Purport']}"
        docs_text.append(Texts)
    return docs_text


def getDocs():
    """
    Extract content from the Data folder, and returns the information
    in Document format.
    """

    docs_doc: list[Document] = []
    for documnt in docs_as_dict():
        content: str = f"{documnt['Translation']} is spoken and "
        content += f"it can be understood using {documnt['Purport']}"
        metadata: dict = {
            key: value for key, value in documnt.items() if key != "Purport"
        }
        metadata["Chapter"], metadata["Verse"] = metadata["Reference"].split(
            ":")
        docs_doc.append(Document(page_content=content, metadata=metadata))

    return docs_doc


def split_docs(docs: list[Document]) -> list[Document]:
    """
    Splits the content of each document into multiple documents based on
    the "\n\n" delimiter.

    Args:
        docs: A list of Document objects.

    Returns:
        A list of new Document objects after splitting.
    """
    split_docs_list = []
    for documnt in docs:
        content = documnt.page_content
        parts = content.split("\n\n")
        for part in parts:
            if part.strip():  # Avoid creating empty documents
                split_docs_list.append(
                    Document(page_content=part, metadata=documnt.metadata)
                )
    return split_docs_list
