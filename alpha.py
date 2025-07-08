import streamlit as st
from src.agents.chat_models import gemini


st.title("RAG Model on Gita")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def extract_text_from_stream(stream):
    for response in stream:
        if hasattr(response, "content"):
            yield response.content


if prompt := st.chat_input("Ask me here.."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [
            (
                "system",
                "You are an smart assistant who give brief and easy to understand response to the user query",
            )
        ] + [(msg["role"], msg["content"]) for msg in st.session_state.messages]
        # print(messages)
        stream = gemini.invoke(messages).content
        st.markdown(stream)
    st.session_state.messages.append({"role": "assistant", "content": stream})
