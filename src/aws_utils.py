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
    client = boto3.client(
        'secretsmanager',
        region_name=Config.REGION_NAME
    )
    api_key = client.get_secret_value(
        SecretId=Config.SECRET_RECORD
    )['SecretString']

    os.environ['GOOGLE_API_KEY'] = json.loads(api_key).get('GOOGLE_API_KEY')


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
            pickle_files = [obj['Key'] for obj in response['Contents'] if not obj['Key'].endswith('/')]
            print("Pickle Files:", pickle_files)
            return(pickle_files)
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

def download_pickles_to_local(local_folder):
    """Download all files from a specified S3 directory to a local directory."""
    files = get_all_pickles()
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
            print("Downloaded")
    except (ClientError, NoCredentialsError) as e:
        print(f'Error downloading files: {e}')

def upload_directory_to_s3(local_folder):
    """
    Upload all files from a local directory to an S3 bucket.
    """
    s3 = get_s3_client()
    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            # Correctly form the s3_path relative to the PICKLE_DIR
            relative_path = os.path.relpath(local_path, start=local_folder)
            s3_path = os.path.join(Config.PICKLE_DIR, relative_path)
            print(f"Uploading {local_path} to {s3_path}...")
            # Fix: changed the third parameter to `s3_path` instead of `Config.PICKLE_DIR`
            s3.upload_file(local_path, Config.BUCKET_NAME, s3_path)
    print("Upload complete.")


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
