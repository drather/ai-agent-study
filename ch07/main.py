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

from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("unsu.pdf")
pages = loader.load_and_split()

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

db = Chroma.from_documents(texts, embeddings_model)

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
result = rag_chain.invoke("아내가 먹고싶어하는 음식이 뭐야?")
print(result)

