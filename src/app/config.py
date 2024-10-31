"""
BITS chatbot
"""
import os


def get_llm_api_key():
    # Darsh, Please insert code here.
    return "AIzaSyBG5TCCSusvqD7sCnrZfz6TgHoRpJJIxXM"  # os.environ.get('LLM_API_KEY')


class Config():
    APP_TITLE: str = 'BITS WILP Smart Assistant'
    LLM_API_KEY: str = get_llm_api_key()
    PICKLE_DOCS_PATH = '/mnt/s3/vectors/'  # To be replaces with S3 logic
    PDF_DOCS_PATH = '/mnt/s3/docs/'  # To be replaces with S3 logic
