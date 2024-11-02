"""
BITS chatbot
"""
import json
import os
import boto3


def get_llm_api_key():
    secret_name = "your-secret-name"  # Replace with your secret name
    region_name = "your-region"       # Replace with your AWS region
    key_name = "GEMINI_API_KEY"       # Replace with the key name in the secret

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    # Retrieve the secret value
    response = client.get_secret_value(SecretId=secret_name)
    secret_string = response['SecretString']

    # Assuming secret_string is a JSON and contains "LLM_API_KEY"
    secret_dict = json.loads(secret_string)
    llm_api_key = secret_dict.get(key_name)

    return llm_api_key


class Config():
    APP_TITLE: str = 'BITS WILP Smart Assistant'
    LLM_API_KEY: str = get_llm_api_key()
    BUCKET_NAME = 'your-bucket-name'
    PDF_DIR = 'pdfs/'
    PICKLE_DIR = 'pickles/'
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
