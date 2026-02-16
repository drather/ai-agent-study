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

# wikipedia 로더
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

print(wiki.name)

# 네이버 뉴스 로더
loader = WebBaseLoader("https://news.naver.com/")
docs = loader.load()

documents = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200).split_documents(docs)
vectordb = FAISS.from_documents(documents, OpenAIEmbeddings())
retriever = vectordb.as_retriever()

# 검생 도구 생성
retriever_tool = create_retriever_tool( retriever, "naver_news_search", "네이버 뉴스 정보가 저장된 벡터 DB, 당일 기사에 대해 궁금하면 이 툴을 사용하세요")

# arXiv 논문 검색 도구
arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200, load_all_available_meta=False)

arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)

print(arxiv.name)

# agent 가 사용할 tool 을 정의하여 tools 에 저장
tools = [wiki, retriever_tool , arxiv]

# agent llm 모델을 openai 로 정의, tools, prompt 를 입력하여 ㅁgent 완성
agent = create_openai_tools_agent(llm=openai, tools=tools, prompt=prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True )

agent_result =  agent_executor.invoke({"input": "오늘 부동산 관련 주요 소식을 알려줘"})
agent_result2 =  agent_executor.invoke({"input": "LLM 최신 논문에 대해 알려줘"})

print(agent_result)
print(agent_result2)
