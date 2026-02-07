from openai import OpenAI
import streamlit as st
from streamlit_chat import message
from components.Sidebar import sidebar
import json
from shared import constants

api_key = "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" 
selected_model = "google/gemma-3-27b-it:free"
OPENROUTER_BASE = "https://openrouter.ai"
OPENROUTER_API_BASE = f"{OPENROUTER_BASE}/api/v1"

st.title("💬 Streamlit GPT")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a knowledgeable and friendly assistant who provides clear, concise answers. Always be helpful and professional."},
        {"role": "assistant", "content": "How can I help you?"}
    ]


with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    
    user_input = a.text_input(
        label="Your message:",
        placeholder="What would you like to say?",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)

for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=msg["role"] == "user", key=i)

if user_input and not api_key:
    st.info("Please click Connect OpenRouter to continue.")

if user_input and api_key:
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    message(user_input, is_user=True)

    client = OpenAI(api_key=api_key, base_url=OPENROUTER_API_BASE)
    
    response = client.chat.completions.create(
        model=selected_model,
        messages=st.session_state.messages,
    )
    
    if type(response) == str:
        response = json.loads(response)
    msg = response["choices"][0]["message"]
    st.session_state.messages.append(msg)
    message(msg["content"])
