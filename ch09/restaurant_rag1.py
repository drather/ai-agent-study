from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import os

from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

current_dir = os.path.dirname(os.path.abspath(__file__))
restaurant_faiss= os.path.join(current_dir, "restaurant-faiss")

loader = TextLoader(f'{current_dir}/restaurant.txt')
documents = loader.load()

text_spliter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
docs = text_spliter.split_documents(documents)

# chunk_size 와 chunk_overlap 을 바탕으로 embedding 벡터 생성.
# chunk_size 는 한 chunk 의 길이를 의미
# chunk_overlap 은 chunk 당 10% ~ 20% 정도를 겹치게 해서 , 문맥이 유실될 경우에 대비
embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)

db = FAISS.from_documents(docs, embeddings)

# embedding 벡터 저장
db.save_local(restaurant_faiss)
print("레스토랑 임베딩 저장 완료", restaurant_faiss)

# index.faiss : faiss 라이브러리가 생성한 인덱스 파일, 벡터 데이터 저장
# index.pkl: 파이썬의 pickle 형식으로 저장된 메타데이터 파일로 인덱스와 관련된 추가정보를 포함

