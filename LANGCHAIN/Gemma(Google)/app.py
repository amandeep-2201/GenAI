#google ai api key
# https://aistudio.google.com/app/apikey

import os
import streamlit as st 
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import create_retrieval_chain

from dotenv import load_dotenv
load_dotenv()

## load groq and google api key from .env  file

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"]=os.getenv("GOOGLE_API_KEY")

st.title("Gemma Model Document Q&A")

llm = ChatGroq(groq_api_key=groq_api_key, model_name = "gemma-7b-it")

prompt=ChatPromptTemplate.from_template(
    """
    Answer the question based on the provided context only.
    Please provide the most accurate response based on the question.
    <context>
    {context}
    <context>
    Questions:{input}
    
    """
)

def vector_embedding():
    
    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./us_census")  #Data Ingestion
        st.session_state.docs = st.session_state.loader.load()  #Document Loading
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size= 1000, chunk_overlap = 200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)
        
prompt1 = st.text_input("Enter questions related to documents here.") 

if st.button("Embed Documents"):
    vector_embedding()
    st.write("Vector Database Ready")
    
import time

if prompt1 : 
    document_chain = create_stuff_documents_chain(llm,prompt)
    retriever = st.session_state.vectors.as_retriever()
    retriever_chain = create_retrieval_chain(retriever,document_chain)
    
    start = time.process_time()
    response = retriever_chain.invoke({"input":prompt1})
    st.write(response['answer'])
    st.write("Time taken : ",time.process_time()-start,"secs")
    
    #with a streamlit expander
    with st.expander("Document Similarity Search"):
        #find the relevat chunks
        for i,doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("------------------------------")
    
       

