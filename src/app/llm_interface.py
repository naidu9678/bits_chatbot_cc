"""
LLM interface methods for Genini.
"""
import os
import pickle
import streamlit as st
from langchain import OpenAI
from langchain.chains.question_answering import load_qa_chain

from app.utils import get_list_of_files
from app.config import Config


@st.cache_data
def load_index(pickle_files: list):
    indices = {}
    for file in pickle_files:
        with open(file, 'rb') as handle:
            index = pickle.load(handle)
            file_name = file.split('/')[-1]
            indices[file_name] = index
    return indices


def generate_response_from_llm(input_text):
    # Load or create document search indexes
    os.environ["OPENAI_API_KEY"] = Config.LLM_API_KEY
    chain = load_qa_chain(OpenAI(), chain_type="stuff", verbose=True)

    document_index_library = load_index(
        get_list_of_files(
            base_path=Config.INDEX_DOCS_PATH,
            format_strs=[".pickle"],
        )
    )

    # Below is an either or situation. In prod we will choose one.
    # Best fit from each doc. Best when multiple docs contain similar info.
    best_fit = []
    for doc_name, index in document_index_library.items():
        # Retrieve the top 3 relevant passages for each document
        top_results = index.similarity_search(input_text, k=3)  # k=3 can be adjusted based on need
        best_fit.extend(top_results)  # Append the relevant chunks to the list
    # ------------------------------------------

    # Variable to track the best document and the best score
    best_document = None
    best_chunk = None
    best_score = float('inf')  # Initialize with a large value (since lower is better)

    # Iterate over each document index
    for doc_name, index in document_index_library.items():
        # Perform similarity search and get the top result for this document
        results = index.similarity_search(input_text, k=1)  # k=1 to get the top result
        
        # Extract the top result and its score
        if results:
            top_result = results[0]
            score = top_result["score"]  # Or use a method to get the score/distance

            # Update if this document is more relevant (lower score)
            if score < best_score:
                best_score = score
                best_document = doc_name
                best_chunk = top_result["text"]  # This is the text or passage of the top chunk
    
    best_fit = document_index_library[best_document]
    # ------------------------------------------
    
    return chain.run(input_documents=best_fit, question=input_text)
