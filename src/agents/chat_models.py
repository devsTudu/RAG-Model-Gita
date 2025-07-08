from langchain_google_genai import ChatGoogleGenerativeAI


# Google Gemini models
gemini = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
gemini_strict = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
