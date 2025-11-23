# streamlit_app.py
import os
import time
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

@st.cache_resource
def load_env_and_openai():
    load_dotenv()
    return OpenAI(api_key=os.environ["OPENAI_API_KEY"])

client = load_env_and_openai()

st.set_page_config(page_title="Adminergy Chatbot Tester", page_icon="💬")

RAG_PROMPT = os.getenv("SYSTEM_PROMPT", """
                          You are a helpful chatbot. You will be assisting employers who are trying to set up a 
                          401(k) plan. They have specific questions about the rules and regulations around sponsoring a 
                          plan for their employees.
                          """)
GENERIC_PROMPT = os.getenv("SYSTEM_PROMPT", "You are a generic helpful chatbot.")

RAG_PROMPT_ID = os.environ["RAG_PROMPT_ID"]
GENERIC_PROMPT_ID = os.environ["GENERIC_PROMPT_ID"]

st.title("Adminergy Chatbot Tester")

use_rag = st.checkbox("Use IRS Docs and Tailored System Prompt", value=True)

history_key = "history_rag" if use_rag else "history_generic"
prompt_id = RAG_PROMPT_ID if use_rag else GENERIC_PROMPT_ID
system_prompt = RAG_PROMPT if use_rag else GENERIC_PROMPT
if history_key not in st.session_state:
    st.session_state[history_key] = []
history = st.session_state[history_key]

for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Ask about 401(k) plan rules…")

if prompt:
    history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build messages list (system + history + new user)
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        resp = client.responses.create(
            prompt={"id": prompt_id},
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
        history.append({"role": "assistant", "content": reply})
        
# Tell me about a plan with fewer than 26 participants.