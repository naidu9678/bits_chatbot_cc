import streamlit as st
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
import json
import os 
from config import Config
import urllib.parse

@st.cache_resource
def get_s3_client():
    # Check if AWS credentials are provided in the environment
    # aws_access_key = Config.AWS_ACCESS_KEY_ID
    # aws_secret_key = Config.AWS_SECRET_ACCESS_KEY

    # if aws_access_key and aws_secret_key:
    #     print("Using AWS credentials from environment variables.")
    #     return boto3.client(
    #         's3',
    #         aws_access_key_id=aws_access_key,
    #         aws_secret_access_key=aws_secret_key
    #     )
    # else:
    print("Using AWS IAM role assigned to the instance.")
    return boto3.client('s3')


def set_env_variable():
    os.environ['GOOGLE_API_KEY'] = json.loads(
    boto3.client('secretsmanager', region_name=Config.REGION_NAME)
    .get_secret_value(SecretId='chatbot/lmm/key')['SecretString']).get('GOOGLE_API_KEY')

def get_all_pdfs():
    """List all PDF files in the specified S3 bucket directory."""
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(
            Bucket=Config.BUCKET_NAME,
            Prefix=Config.PDF_DIR
        )
        if 'Contents' in response:
            pdf_files = [obj['Key'] for obj in response['Contents']]
            print("PDF Files:", pdf_files)
            return(pdf_files)
        else:
            print("No PDF files found.")
    except (ClientError, NoCredentialsError) as e:
        print(f'Error fetching PDFs: {e}')


def get_all_pickles():
    """List all Pickle files in the specified S3 bucket directory."""
    try:
        s3 = get_s3_client()
        response = s3.list_objects_v2(
            Bucket=Config.BUCKET_NAME,
            Prefix=Config.PICKLE_DIR
        )
        if 'Contents' in response:
            pickle_files = [obj['Key'] for obj in response['Contents']]
            print("Pickle Files:", pickle_files)
        else:
            print("No Pickle files found.")
    except (ClientError, NoCredentialsError) as e:
        print(f'Error fetching Pickles: {e}')
        
def download_files_to_local(local_folder):
    """Download all files from a specified S3 directory to a local directory."""
    files = get_all_pdfs()
    os.makedirs(local_folder, exist_ok=True)

    try:
        s3 = get_s3_client()
        for file_key in files:
            # Encode the file key to handle spaces and special characters
            # encoded_file_key = urllib.parse.quote(file_key)
            # print(encoded_file_key)
            file_name = os.path.basename(file_key)
            local_path = os.path.join(local_folder, file_name)
            print(f"Downloading {file_key} to {local_path}")

            # Download the file using the URL-encoded key
            s3.download_file(
                Config.BUCKET_NAME,
                file_key,
                local_path
            )
    except (ClientError, NoCredentialsError) as e:
        print(f'Error downloading files: {e}')

def add_pickle(file_name, file_path):
    """Upload a Pickle file to the specified S3 bucket directory."""
    try:
        s3 = get_s3_client()
        s3.upload_file(
            file_path,
            Config.BUCKET_NAME,
            f"{Config.PICKLE_DIR}{file_name}"
        )
        print(f"Uploaded {file_name} to {Config.PICKLE_DIR}")
    except (ClientError, NoCredentialsError) as e:
        print(f"Could not upload {file_name}: {e}")


def delete_pickle(file_name):
    """Delete a Pickle file from the specified S3 bucket directory."""
    try:
        s3 = get_s3_client()
        s3.delete_object(
            Bucket=Config.BUCKET_NAME,
            Key=f"{Config.PICKLE_DIR}{file_name}"
        )
        print(f"Deleted {file_name} from {Config.PICKLE_DIR}")
    except (ClientError, NoCredentialsError) as e:
        print(f"Could not delete {file_name}: {e}")


def add_pdf(file_name, file_path):
    """Upload a PDF file to the specified S3 bucket directory."""
    try:
        s3 = get_s3_client()
        s3.upload_file(
            file_path,
            Config.BUCKET_NAME,
            f"{Config.PDF_DIR}{file_name}"
        )
        print(f"Uploaded {file_name} to {Config.PDF_DIR}")
    except (ClientError, NoCredentialsError) as e:
        print(f"Could not upload {file_name}: {e}")
