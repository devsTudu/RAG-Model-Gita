from abc import ABC, abstractmethod
from app.webapp.dataclass import model_query

from src.vector_store.load_db import SECONDARY_DB, PRIMARY_DB, Robust
from src.agents.chat_models import gemini, gemini_strict


LLM = gemini
LLM_S = gemini_strict
RETRIEVER = Robust

TEMPLATES: dict[str, str] = {
    "BASIC": """You are a wise and empathetic guide helping a user understand the teachings of the Bhagavad Gita.
                Use the retrieved context, which are from 'the Bhagavad Gita - As it is' Book, below to answer the user's question.
                If the context provides sufficient information, respond with clarity and depth. Use analogies or real-life examples
                to make difficult concepts more relatable.
                If the context seems insufficient to fully answer the user's question, acknowledge it respectfully, and 
                suggest how the user might explore it further or request clarification.
                Always maintain a tone that is humble, respectful, and spiritually aware.
                Context:
                {context}
                User’s Question:
                {question}
                Your Answer: """.strip(),
    "query_generate": """You are an AI language model assistant. Your task is to generate {n}
            different versions of the given user question to retrieve relevant documents from a vector
            database. By generating multiple perspectives on the user question, your goal is to help
            the user overcome some of the limitations of the distance-based similarity search.
            Provide these alternative questions separated by newlines. Original question: {question} \n
            Output ({n} queries): """,
}


class RAG_Model(ABC):
    """The Abstract class for building RAGs

    Args:
        ABC (_type_): Abstract Base Class
    """

    def __init__(self, query: model_query) -> None:
        self.query = query

    @abstractmethod
    def process(self) -> str:
        """"""
        pass

    def cleaned(self) -> str:
        response = self.process()
        if isinstance(response, str):
            response.replace("provided text", "Bhagavad Gita")
        return response
