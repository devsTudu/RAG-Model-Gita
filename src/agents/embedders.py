from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.environmentVariablesHandler import get

myEmbedder = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=get("GOOGLE_API_KEY")  # type: ignore
)
