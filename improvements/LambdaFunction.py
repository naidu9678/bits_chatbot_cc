import os
import boto3
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from aws_utils import set_env_variable

s3_client = boto3.client('s3')


def download_directory_from_s3(bucket_name, s3_prefix, local_folder):
    """
    Download an entire directory from an S3 bucket to a local path.
    """
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix)
    if 'Contents' in response:
        for obj in response['Contents']:
            key = obj['Key']
            file_name = key.split('/')[-1]
            if file_name:  # Avoiding directories
                s3_client.download_file(bucket_name, key, os.path.join(local_folder, file_name))


def upload_directory_to_s3(bucket_name, local_folder, s3_prefix):
    """
    Upload all files from a local directory to an S3 bucket.
    """
    for root, _, files in os.walk(local_folder):
        for file in files:
            local_path = os.path.join(root, file)
            s3_path = os.path.join(s3_prefix, file)
            s3_client.upload_file(local_path, bucket_name, s3_path)


def load_pdfs_to_vectorstore(pdf_paths, faiss_index_path):
    """
    Load multiple PDFs and create/update the FAISS vector store.
    """
    # Set required environment variables for gemini api key
    set_env_variable()

    try:
        # Create embeddings
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        # Load existing FAISS index if available
        if os.path.exists(faiss_index_path):
            vectorstore = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)
        else:
            vectorstore = FAISS(embedding_model=embedding_model)

        for pdf_path in pdf_paths:
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            data = loader.load()

            # Split text
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
            docs = text_splitter.split_documents(data)

            # Add new documents to the vector store
            vectorstore.add_documents(docs)

        # Save the updated vector store
        vectorstore.save_local(faiss_index_path)

        return vectorstore
    except Exception as e:
        raise Exception(f"Error loading PDFs into vector store: {e}")


def lambda_handler(event, context):
    bucket_name = 'bits-wilp-chatbot-assignment1'
    pdfs_s3_prefix = 'resources/'
    pickles_s3_prefix = 'pickles/'

    pdfs_folder = '/tmp/pdfs'
    pickles_folder = '/tmp/pickles'

    # Download PDF and existing pickle files from S3
    download_directory_from_s3(bucket_name, pdfs_s3_prefix, pdfs_folder)
    download_directory_from_s3(bucket_name, pickles_s3_prefix, pickles_folder)

    # Set FAISS index path in the local pickles folder
    # faiss_index_path = os.path.join(pickles_folder, 'faiss_index')

    # Collect all PDF file paths
    pdf_files = [os.path.join(pdfs_folder, filename) for filename in os.listdir(pdfs_folder) if filename.endswith('.pdf')]

    try:
        updated_vectorstore = load_pdfs_to_vectorstore(pdf_files, pickles_folder)
        print("PDFs loaded successfully into the vector store.")

        # Upload Pickles directory (FAISS index files) to S3
        upload_directory_to_s3(bucket_name, pickles_folder, pickles_s3_prefix)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up: delete the /tmp directories
        if os.path.exists(pdfs_folder):
            shutil.rmtree(pdfs_folder)
            print(f"Deleted {pdfs_folder} and its contents.")
        if os.path.exists(pickles_folder):
            shutil.rmtree(pickles_folder)
            print(f"Deleted {pickles_folder} and its contents.")