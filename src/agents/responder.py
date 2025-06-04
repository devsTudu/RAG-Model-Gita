from abc import ABC, abstractmethod
from app.dataclass import model_query
from src.vector_store.load_db import Neon_DB,Supabase_DB
from src.agents.chat_models import gemini,gemini_strict

from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser



LLM = gemini
LLM_S = gemini_strict


class RAG_Model(ABC):
    """The Abstract class for building RAGs

    Args:
        ABC (_type_): Abstract Base Class
    """
    def __init__(self,query:model_query) -> None:
        self.query = query
        
    
    
    @abstractmethod
    def process(self)-> str:
        """"""
        pass
    
    
MODEL_REGISTRY: dict[str, type[RAG_Model]] = {}

def register_model(name: str):
    def wrapper(cls: type[RAG_Model]):
        MODEL_REGISTRY[name] = cls
        return cls
    return wrapper

@register_model('naive')
class naive(RAG_Model):
    def __init__(self, query: model_query) -> None:
        super().__init__(query)
    
    def process(self) -> str:
        template = """You are a wise and empathetic guide helping a user understand the teachings of the Bhagavad Gita.
                    Use the retrieved context, which are from 'the Bhagavad Gita - As it is' Book, below to answer the user's question. If the context provides sufficient information, respond with clarity and depth. Use analogies or real-life examples to make difficult concepts more relatable.

                    If the context seems insufficient to fully answer the user's question, acknowledge it respectfully, and suggest how the user might explore it further or request clarification.

                    Always maintain a tone that is humble, respectful, and spiritually aware.

                    Context:
                    {context}

                    User’s Question:
                    {query}

                    Your Answer:
        """.strip()
        prompt = ChatPromptTemplate.from_template(template)
        retriever = Neon_DB.get_retriever()
        rag_chain = (
            {"context": retriever, "query": RunnablePassthrough()}
            | prompt
            | LLM
            | StrOutputParser()
        )

        return rag_chain.invoke(self.query.query).replace("provided text","Bhagavad Gita")

@register_model('HyDe')
class hyde(RAG_Model):
    def __init__(self, query: model_query) -> None:
        super().__init__(query)
    
    def process(self) -> str:
        template = """Please write a scientific logical explanation paper passage to answer the question,
        focus more on the understanding and influence of the answer to the audience than the fact,
        Question: {question}
        Passage:"""
        prompt_hyde = ChatPromptTemplate.from_template(template)

        generate_docs_for_retrieval = (
            prompt_hyde | LLM_S | StrOutputParser()
        )

        def Hyde_response(question):
            # question = "What is task decomposition for LLM agents?"
            generate_docs_for_retrieval.invoke({"question":question})
            retriever = Supabase_DB.get_retriever()
            retrieval_chain = generate_docs_for_retrieval | retriever
            retrieved_docs = retrieval_chain.invoke({"question":question})
            # RAG
            template = """Answer the following question based on this context:

            {context}

            Question: {question}
            """

            prompt = ChatPromptTemplate.from_template(template)

            final_rag_chain = (
                prompt
                | LLM
                | StrOutputParser()
            )
            return final_rag_chain.invoke({"context":retrieved_docs,"question":question})

        
        return Hyde_response(self.query.query)


list_models = list(MODEL_REGISTRY.keys())