from langchain_google_genai import GoogleGenerativeAIEmbeddings

myEmbedder = GoogleGenerativeAIEmbeddings(
    model='models/embedding-001'
)
