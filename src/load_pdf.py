"""
Checks for pdf files and generates and store corresponding
indices in pickel files.
"""
import os
import pickle
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain import FAISS

from app.utils import get_list_of_files
from app.config import Config


def read_pdf(pdf_file):
    pdfreader = PdfReader(pdf_file)
    raw_text = ''
    for page in pdfreader.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=600000,
        chunk_overlap=200,
        length_function=len
    )

    texts = text_splitter.split_text(raw_text)
    return texts


def gen_index_doc(pdf_file):
    text = read_pdf(pdf_file)
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    document_index = FAISS.from_texts(text, embeddings)
    pickle_path = Config.PICKLE_DOCS_PATH + os.path.basename(pdf_file).replace(".pdf", ".pickle")
    with open(pickle_path, 'wb') as f:
        pickle.dump(document_index, f, pickle.HIGHEST_PROTOCOL)
    
    return pickle_path


def main():
    list_of_pdfs = get_list_of_files(
        base_path=Config.PDF_DOCS_PATH,
        format_strs=[".pdf"],
    )
    list_of_pickles = get_list_of_files(
        base_path=Config.PICKLE_DOCS_PATH,
        format_strs=['.pickle']
    )

    for pdf_file in list_of_pdfs:
        file_name = os.path.splitext(os.path.basename(pdf_file))[0]
        corr_pickle = os.pat.join(
            Config.PICKLE_DOCS_PATH,
            file_name + ".pickle"
        )

        if corr_pickle in list_of_pickles:
            list_of_pickles.remove(corr_pickle)
        else:
            print(f"Generating index for {file_name}.pickle")
            gen_index_doc(pdf_file=pdf_file)
    
    for pickle_file in list_of_pickles:
        print(f"Deleting {pickle_file}")
        os.remove(pickle_file)


if __name__ == '__main__':
    main()
