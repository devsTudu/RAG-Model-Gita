from dotenv import load_dotenv
load_dotenv()

from src.agents.responder import multi_query_fusion
from app.webapp.dataclass import model_query
from src.agents.search import search_for


query = "What is the goal of life?"
agent = multi_query_fusion(query=model_query(model='deep_1',
                                           question=query))

print(agent.cleaned())