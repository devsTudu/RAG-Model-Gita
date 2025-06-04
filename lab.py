from dotenv import load_dotenv
load_dotenv()

from src.agents.chat_models import gemini

query = [
    ("system", "Translate the user sentence to French."),
    ("human", "I love programming."),
]

data = gemini.invoke(query)
print(data)
# print(knowledge[0])
