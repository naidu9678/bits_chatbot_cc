import streamlit as st
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import faiss 

load_dotenv()

st.title("BITS WILP Smart AI Assistant")

# Initialize session state variables
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
    st.session_state.chat_history = []

# Load PDF and create vector store if not already done
if st.session_state.vectorstore is None:
    # Load PDF
    loader = PyPDFLoader("Cloud_Computing.pdf")
    data = loader.load()

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
    docs = text_splitter.split_documents(data)

    # Create embeddings and FAISS vector store
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents=docs, embedding=embedding_model)
    st.session_state.vectorstore = vectorstore

# Set up retriever
retriever = st.session_state.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 10})

# Set up LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, max_tokens=None, timeout=None)

# Set up prompt template
system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Input and Response
query = st.chat_input("Ask something: ")
if query:
    # Append the query to chat history
    st.session_state.chat_history.append({"user": query})

    with st.spinner("Processing your request..."):
        try:
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)

            response = rag_chain.invoke({"input": query})

            # Append the assistant's response to chat history
            st.session_state.chat_history.append({"assistant": response["answer"]})

            # Display chat history
            for chat in st.session_state.chat_history:
                if "user" in chat:
                    st.write(f"**You:** {chat['user']}")
                elif "assistant" in chat:
                    st.write(f"**Assistant:** {chat['assistant']}")

        except Exception as e:
            st.error(f"An error occurred: {e}")
