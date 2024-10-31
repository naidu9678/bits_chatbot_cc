import PyPDF2
from PyPDF2 import PdfReader
from langchain import OpenAI, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import streamlit as st
import os
import pickle

st.title('BITS WILP Smart Assistant')
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

openai_api_key = ""
os.environ['OPENAI_API_KEY'] = openai_api_key


@st.cache_data
def prepare_embeddings(model, chain_type):
    embeddings = OpenAIEmbeddings(model=model)
    chain = load_qa_chain(OpenAI(), chain_type=chain_type, verbose=True)
    return embeddings, chain


#embeddings, chain = prepare_embeddings(model="text-embedding-ada-002", chain_type="stuff")

def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text

def read_multiple_pdfs(folder_path):
    pdf_contents = ''
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            pdf_text = read_pdf(file_path)
            pdf_contents+=pdf_text

            # pdf_contents.append(pdf_text)
    return pdf_contents

# Replace 'folder_path' with the path to the folder containing your PDF files
folder_path = './resource'
pdf_contents = ''

def generate_response_from_openAI(input_text):
    try:
        with open('document_search_log1.pickle', 'rb') as f:
            document_search_batch = pickle.load(f)
    except:
        pdf_text1 = pdf_reader("./resource/batch_sg_log.pdf")
        document_search_batch = FAISS.from_texts(pdf_text1, embeddings)
        with open('document_search_log1.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(document_search_batch, f, pickle.HIGHEST_PROTOCOL)

    try:
        with open('document_search_log2.pickle', 'rb') as f:
            document_search_expi = pickle.load(f)
    except:
        pdf_text2 = pdf_reader("./resource/expi_log.pdf")
        document_search_expi = FAISS.from_texts(pdf_text2, embeddings)
        with open('document_search_log2.pickle', 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(document_search_expi, f, pickle.HIGHEST_PROTOCOL)

    document_search_batch.merge_from(document_search_expi)
    docs = document_search_batch.similarity_search(input_text)
    print(docs)

    result = chain.run(input_documents=docs, question=input_text)

    if input_text:
        return result


def pdf_reader(pdf_file):
    pdfreader = PdfReader(pdf_file)

    # read txt from pdf
    raw_text = ''

    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    # we need to split text using character text splitter so that it does not increase token size

    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=600000,
        chunk_overlap=200,
        length_function=len
    )

    texts = text_splitter.split_text(raw_text)
    return texts


if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
   # pdf_contents = read_multiple_pdfs(folder_path)
   # msg = generate_response_from_openAI(prompt)
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)