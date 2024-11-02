# app/views.py
import streamlit as st

from app.llm_interface import generate_response_from_llm
from app.config import Config


def render_ui():
    st.title(Config.APP_TITLE)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{
            "role": "assistant",
            "content": "How can I help you?"
        }]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    # Chat prompt input
    if prompt := st.chat_input():

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Generate response
        msg = generate_response_from_llm(prompt)
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
