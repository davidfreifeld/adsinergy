# streamlit_app.py
import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

loaded = load_dotenv()

st.set_page_config(page_title="Chatbot Test Arena", page_icon="💬", layout="wide")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", """
                          You are a helpful chatbot. You will be assisting employers who are trying to set up a 
                          401(k) plan. They have specific questions about the rules and regulations around sponsoring a 
                          plan for their employees.
                          """)
RAG_PROMPT_ID = os.getenv("RAG_PROMPT_ID")
GENERIC_PROMPT_ID = os.getenv("GENERIC_PROMPT_ID")

st.title("Chatbot Test Arena")

st.header("With IRS Docs")
if "history_rag" not in st.session_state:
    st.session_state.history_rag = []
for m in st.session_state.history_rag:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask about 401(k) plan rules…")

if prompt:
    st.session_state.history_rag.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build messages list (system + history_rag + new user)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(st.session_state.history_rag)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        resp = client.responses.create(
            prompt={"id": RAG_PROMPT_ID},
            input=messages,
            # tools=[
            #     {
            #         "type": "file_search",
            #         "vector_store_ids": [VECTOR_STORE_ID]
            #     }
            # ]
        )

        # Poll until done
        while resp.status in {"queued", "in_progress"}:
            time.sleep(0.5)
            resp = client.responses.get(resp.id)

        # Extract text (first part)
        reply = resp.output_text
        placeholder.markdown(reply)
        st.session_state.history_rag.append({"role": "assistant", "content": reply})
        
# Tell me about a plan with fewer than 26 participants.