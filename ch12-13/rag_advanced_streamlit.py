import os
import tempfile
import streamlit as st
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.document_loaders import PyPDFLoader
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_classic.retrievers import BM25Retriever, EnsembleRetriever
from langchain_core.output_parsers import StrOutputParser
from streamlit_extras.buy_me_a_coffee import button
from langchain_classic.load import dumps, loads
from langchain_community.vectorstores import FAISS
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore


button(username="drather", floating=True, width=221)

st.title("chatPDF with Multiquery + hybridSearc + RagFusion")
st.write("---")
st.write("PDF 파일을 업로드하고 내용을 기반으로 질문하세요 ")

openai_key = st.text_input("openai key 를 입력해해주세요", type="password")

model_choice = st.selectbox(
    ' 사용할 GPT 모델을 선택하세요',
    ['gpt-3.5-turbo', 'gpt-4o-mini', 'gpt-4o']
)

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요. ", type=["pdf"])
st.wrtie("---")

# PDF 를 문서로 변환하는 함수
def pdf_to_document(uploaded_file):
    temp_dir = tempfile.TemporaryDirectory()
    temp_filepath = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_filepath, "wb") as f:
        f.write(uploaded_file.getvalue())
    loader = PyPDFLoader(temp_filepath)
    pages = loader.load_and_split()
    return pages

# 문서를 포매팅
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# 파일 업로드 확인
if uploaded_file is not None:
    pages = pdf_to_document(uploaded_file)

    # 문서를 청크로 분할
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=500,
        chunk_overlap=50
    )

    splits = text_splitter.split_documents(pages)

