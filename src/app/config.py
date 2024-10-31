"""
BITS chatbot
"""
import json
import os
import boto3
from botocore.exceptions import ClientError


def get_llm_api_key():
    secret_name = "your-secret-name"  # Replace with your secret name
    region_name = "your-region"       # Replace with your AWS region
    key_name = "GEMINI_API_KEY"       # Replace with the key name in the secret

    # Create a Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region_name)

    try:
        # Retrieve the secret value
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']

        # Assuming secret_string is a JSON and contains "LLM_API_KEY"
        secret_dict = json.loads(secret_string)
        llm_api_key = secret_dict.get(key_name)

        if llm_api_key:
            os.environ['LLM_API_KEY'] = llm_api_key
            print("LLM_API_KEY successfully set.")
        else:
            print("LLM_API_KEY not found in the secret.")

    except ClientError as e:
        print(f"Error retrieving secret {secret_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Althought the key is set in environment, Just returning the value if in case to be called from other modules   
    return os.getenv('LLM_API_KEY')

class Config():
    APP_TITLE: str = 'BITS WILP Smart Assistant'
    LLM_API_KEY: str = get_llm_api_key()
    PICKLE_DOCS_PATH = '/mnt/s3/vectors/'  # To be replaces with S3 logic
    PDF_DOCS_PATH = '/mnt/s3/docs/'  # To be replaces with S3 logic
