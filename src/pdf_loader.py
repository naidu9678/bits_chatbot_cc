# pdf_loader.py

import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from aws_utils import download_files_to_local, set_env_variable


def load_pdfs_to_vectorstore(pdf_paths, faiss_index_path):
    """
    Load multiple PDFs and create/update the FAISS vector store.

    :param pdf_paths: List of paths to the PDF files.
    :param faiss_index_path: Path to save/load the FAISS index.
    :return: The updated FAISS vector store.
    """

    # Set required environment variables for gemini api key
    set_env_variable()


    try:
        # Create embeddings
        embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)

        # # Define the embedding dimension (replace 512 with the correct dimension)
        # embedding_dim = 512  # Assume the embedding dimension is known

        # # Check if FAISS index exists; if not, create a new one
        # if os.path.exists(faiss_index_path):
        #     vectorstore = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)
        # else:
        #     index = faiss.IndexFlatL2(embedding_dim)  # Initialize based on embedding dimension
        #     vectorstore = FAISS(index, embedding_model)

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

if __name__ == "__main__":
    # Define the folder containing PDF files
    pdfs_folder = "static/pdfs"  # Path to your PDFs folder
    faiss_index_path = "static/faiss_index"  # Path to your FAISS index file
    download_files_to_local(pdfs_folder)

    # os.makedirs('static/faiss_index', exist_ok=True)

    # Collect all PDF file paths from the specified folder
    pdf_files = [os.path.join(pdfs_folder, filename) for filename in os.listdir(pdfs_folder) if filename.endswith('.pdf')]
    
    try:
        updated_vectorstore = load_pdfs_to_vectorstore(pdf_files, faiss_index_path)
        print("PDFs loaded successfully into the vector store.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up: Delete the static/pdfs directory and its contents
        if os.path.exists(pdfs_folder):
            shutil.rmtree(pdfs_folder)
            print(f"Deleted {pdfs_folder} and its contents.")    
