import sys

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import tempfile


from langchain_community.document_loaders import PyPDFLoader
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
import langchainhub as hub
from langchain_core.output_parsers import StrOutputParser
import json
from langsmith import Client
from langchain_core.load import loads
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

st.title("ChatPDF")
st.write("---")

uploaded_file = st.file_uploader("PDF 파일을 올려주세요" , type=['pdf'])
st.write("---")

def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
        loader = PyPDFLoader(temp_filepath)
        pages = loader.load_and_split()
        return pages

if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)

    text_spliter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False
    )

    texts = text_spliter.split_documents(pages)

    embeddings_model = OpenAIEmbeddings(
        model="text-embedding-3-large",
        # With the 'text-embedding-3' class
        # of the models, you can specify the size of the embeddings you want returned.
        dimensions=1024
    )

    import chromadb
    chromadb.api.ClientAPI.clear_system_cache()

    db = Chroma.from_documents(texts, embeddings_model)

    st.header("PDF 에게 질문해보세요")
    question = st.text_input("질문을 입력하세요")

    if st.button("질문하기"):
        with st.spinner('Wait for it'):
            llm = ChatOpenAI(temperature=0)

            retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db.as_retriever(), llm=llm)

            client = Client()

            # hub.pull() 메서드가 동작하지 않아, 수정하여 진행
            prompt = client.pull_prompt("rlm/rag-prompt")

            # 생성기
            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            rag_chain = (
                {"context": retriever_from_llm | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            # Question
            result = rag_chain.invoke(question)
            st.write(result)
