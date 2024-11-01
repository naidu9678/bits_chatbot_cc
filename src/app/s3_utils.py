import streamlit as st
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

from app.config import Config


@st.cache_resource
def get_s3_client():
    # Check if AWS credentials are provided in the environment
    aws_access_key = Config.AWS_ACCESS_KEY_ID
    aws_secret_key = Config.AWS_SECRET_ACCESS_KEY

    if aws_access_key and aws_secret_key:
        print("Using AWS credentials from environment variables.")
        return boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
    else:
        print("Using AWS IAM role assigned to the instance.")
        return boto3.client('s3')


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
