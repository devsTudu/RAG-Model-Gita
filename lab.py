from dotenv import load_dotenv
load_dotenv()

from src.agents.responder import multi_query_fusion
from app.webapp.dataclass import model_query

# print(custom_model.invoke("What is the capital of France?"))

agent = multi_query_fusion(query=model_query(model='any',
                                           question='What is the goal of life?'))

print(agent.cleaned())