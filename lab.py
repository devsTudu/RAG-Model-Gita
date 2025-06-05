from dotenv import load_dotenv
load_dotenv()

from src.agents.responder import multi_query_fusion
from app.webapp.dataclass import model_query

agent = multi_query_fusion(query=model_query(model='any',
                                           question='What is the goal of life?'))

print(agent.cleaned())