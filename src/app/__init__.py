"""
Application Factory to create and configure the Streamlit app.
"""
import streamlit as st
from app.views import render_ui
from app.config import Config


def create_app():
    st.set_page_config(page_title=Config.APP_TITLE)
   
    render_ui()
