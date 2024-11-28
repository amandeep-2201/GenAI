'''
Object Box : 
Own your data. Own your AI. Offline-first. 
Access your data when and where needed, with 
or without internet connectivity. The ObjectBox 
highspeed database securely stores your data 
privately on-device and syncs it seamlessly with 
millions of devices on-premise and optionally with 
any cloud.
'''

import streamlit as st 
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_objectbox.vectorstores import ObjectBox
from langchain_community.document_loaders import PyPDFDirectoryLoader

#load groq and open ai API key

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
groq_api_key=os.getenv("GROQ_API_KEY")

st.title("Objectbox VectorstoreDB with Llama3(Groq) demo")

#llm = ChatGroq(model_name = "llama3-8b-8192")
llm = ChatGroq(groq_api_key = groq_api_key, model_name = "llama3-8b-8192")

prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Questions:{input}
    """
)

## Creatign Vector Embedding and Object Vectorstore db

def vector_embedding():
    
    if "vectors" not in st.session_state:
        st.session_state.loader=PyPDFDirectoryLoader("./us_census")
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:20])
        st.session_state.embeddings = OpenAIEmbeddings()
        st.session_state.vectors = ObjectBox.from_documents(st.session_state.final_documents,st.session_state.embeddings, embedding_dimensions=768)


input_prompt = st.text_input("Enter Your Question From Documents")

if st.button("Documents Embedding"):
    vector_embedding()
    st.write("ObjectBox Database is ready.")
    
import time

#create_stuff_documents_chain will be responsible for providing the context
#create retrieval chain will help us to invoke the llm

if input_prompt:
    document_chain = create_stuff_documents_chain(llm, prompt)
    retriever = st.session_state.vectors.as_retriever()
    retrieval_chain =  create_retrieval_chain(retriever, document_chain)
    
    start = time.process_time()
    response = retrieval_chain.invoke({"input": input_prompt})
    #print("Response time : ",time.process_time()-start)
    st.write("Response time : ",time.process_time()-start)
    st.write(response['answer'])
    
    #with a streamlit expander
    with st.expander("Document Similarity Search"):
        #Find the relevant chunks
        for i, doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("-----------------------------")













