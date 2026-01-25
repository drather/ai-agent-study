import asyncio

from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import os

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

current_dir = os.path.dirname(os.path.abspath(__file__))

async def main():
    # 환경변수에서 가져온 openai api 키를 사용하여 OpenaiEmbeddings 클래스 초기화
    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

    # 지정된 임베딩을 사용하여 로컬에 저장된 faiss 클래스를 로드
    # allow_dangerous_deserialization=True 옵션 통한 직렬화 허용
    load_db = FAISS.load_local(f'{current_dir}/restaurant-faiss', embeddings, allow_dangerous_deserialization=True)

    query = "음식점의 룸 서비스는 어떻게 운영되나요? "
    print(query)

    result = load_db.similarity_search(query, k=2)

    embedding_vector_query = embeddings.embed_query(query)
    print("query vector: ", embedding_vector_query, "\n")

    docs = await load_db.asimilarity_search_by_vector(embedding_vector_query)

    print(docs[0])



if __name__ == '__main__':
    asyncio.run(main())
