import uvicorn
from fastapi import FastAPI
import os
from dotenv import load_dotenv
import chromadb
import base64
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from datasets import load_dataset
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes
from langchain_ollama import OllamaLLM


from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Langchain Server",
    version="0.1",
    description="simple langchain API Server"
)

openAiModel = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    temperature=0.7,
    model='gpt-3.5-turbo'
)

llamaModel = OllamaLLM(model="llama3.1:8b")

prompt = ChatPromptTemplate.from_template("한국어로 담변을 장성해줘 {input}")

prompt2 = ChatPromptTemplate.from_template("주제에 맞는 소설을 작성해줘. 500자 이내로 작성해줘 {topic}")

prompt3 = ChatPromptTemplate.from_template("주제에 맞는 시를 작성해줘. 200자 이내로 작성해줘 {topic}")

add_routes(
    app,
    prompt | openAiModel ,
    path="/openai"
   )
add_routes(
    app,
    prompt | llamaModel,
    path="/llama",
)

add_routes(
    app,
    prompt2| openAiModel,
    path="/openai/novel"
)

add_routes(
    app,
    prompt3| openAiModel,
    path="/openai/poem"
)

add_routes(
    app, prompt3 | llamaModel, path="/llama/novel"
)

add_routes(
    app, prompt3 | llamaModel,  path="/llama/poem"
)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)