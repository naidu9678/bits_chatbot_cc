"""
BITS chatbot
"""

class Config():
    APP_TITLE: str = 'BITS WILP Smart Assistant'
    REGION_NAME='us-east-1'
    BUCKET_NAME = 'bits-wilp-chatbot-assignment1'
    PDF_DIR = 'resources/'
    PICKLE_DIR = 'pickles/'
    SECRET_RECORD='chatbot/gemini/api/key'
    # AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    # AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')