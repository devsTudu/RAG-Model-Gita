from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.load import dumps, loads

from operator import itemgetter

from app.webapp.dataclass import model_query
from src.agents.base import RAG_Model, TEMPLATES, RETRIEVER, LLM, LLM_S

MODEL_REGISTRY: dict[str, type[RAG_Model]] = {}

def register_model(name: str):
    def wrapper(cls: type[RAG_Model]):
        MODEL_REGISTRY[name] = cls
        return cls
    return wrapper


@register_model(name='quick_1')
class naive(RAG_Model):
    """The most general and simple RAG Model

    Args:
        RAG_Model (_type_): _description_
    """
    def process(self) -> str:
        template = TEMPLATES['BASIC']
        prompt = ChatPromptTemplate.from_template(template)
        rag_chain = (
            {"context": RETRIEVER, "question": RunnablePassthrough()}
            | prompt
            | LLM
            | StrOutputParser()
        )

        return rag_chain.invoke(self.query.question)

@register_model('quick_2')
class hyde(RAG_Model):
    """Model with Hypothetical Document Embedding techniques

    Args:
        RAG_Model (_type_): _description_
    """
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
            retrieval_chain = generate_docs_for_retrieval | RETRIEVER
            retrieved_docs = retrieval_chain.invoke({"question":question})
            # RAG
            template = TEMPLATES["BASIC"]

            prompt = ChatPromptTemplate.from_template(template)

            final_rag_chain = (
                prompt
                | LLM
                | StrOutputParser()
            )
            return final_rag_chain.invoke({"context":retrieved_docs,"question":question})
        return Hyde_response(self.query.question)

@register_model('deep_1')
class multi_query_fusion(RAG_Model):

    
    def reciprocal_rank_fusion(self,results: list[list], k=60):
        """ Reciprocal_rank_fusion that takes multiple lists of ranked documents
            and an optional parameter k used in the RRF formula """

        # Initialize a dictionary to hold fused scores for each unique document
        fused_scores = {}

        # Iterate through each list of ranked documents
        for docs in results:
            # Iterate through each document in the list, with its rank (position in the list)
            for rank, doc in enumerate(docs):
                # Convert the document to a string format to use as a key (assumes documents can be serialized to JSON)
                doc_str = dumps(doc)
                # If the document is not yet in the fused_scores dictionary, add it with an initial score of 0
                if doc_str not in fused_scores:
                    fused_scores[doc_str] = 0
                # Retrieve the current score of the document, if any
                previous_score = fused_scores[doc_str]
                # Update the score of the document using the RRF formula: 1 / (rank + k)
                fused_scores[doc_str] += 1 / (rank + k)

        # Sort the documents based on their fused scores in descending order to get the final reranked results
        reranked_results = [
            (loads(doc), score)
            for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
        ]

        # Return the reranked results as a list of tuples, each containing the document and its fused score
        return reranked_results
    
    def process(self) -> str:
        template = TEMPLATES["query_generate"]
        prompt = ChatPromptTemplate.from_template(template)
        generate_queries = (
            {"n":itemgetter("n"),'question':itemgetter("question")}
            | prompt
            | LLM_S
            | StrOutputParser()
            | (lambda x: x.split('\n'))
        )
        
        retrieval_chain_rag_fusion = (
            generate_queries
            | RETRIEVER.map()
            | self.reciprocal_rank_fusion
        )
        prompt = ChatPromptTemplate.from_template(TEMPLATES['BASIC'])
        rag_chain_fusion = (
            {"context": retrieval_chain_rag_fusion,"question":itemgetter("question")}
            | prompt
            | LLM
            | StrOutputParser()
        )
        return rag_chain_fusion.invoke({"question":self.query.question,"n":"five"})


list_models = list(MODEL_REGISTRY.keys())

async def get_response(query:model_query):
    """Get the response for the query

    Args:
        query (model_query): The request received

    Returns:
        str: The Models response to the question
    """
    model = MODEL_REGISTRY.get(query.model,naive)
    response = model(query).cleaned()
    return response