# Agents 생성을 위한 참조 Agent Executer
from langchain.agents import AgentExecutor

# 벡터 DB를 agent에게 전달하기 위한 tool생성
from langchain.agents import create_openai_tools_agent

# langchainhub 에서 제공하는 prompt 사용
from langchain import hub

# arxiv 논문 검색을 위한 tool 생성
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun

# 벡터 DB구축 및 검색 도구
from langchain.tools.retriever import create_retriever_tool
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

# langchain 공식 문서 검색을 위한 검색기 역할을 하는 벡터 DB 생성
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader

# agent tools 중 wikipedia 사용
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

#openAI LLM 설정
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

# 일관된 값을 위하여 Temperature 0.1로 설정 model은 gpt-4o로도 설정 할 수 있습니다.
openai = ChatOpenAI(
    model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0.1)

prompt = hub.pull("hwchase17/openai-functions-agent")

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)

wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

print(wiki.name)
