from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
import os

from dotenv import load_dotenv

from ch07.main import text_spliter

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

current_dir = os.path.dirname(os.path.abspath(__file__))

restaurant_faiss= os.path.join(current_dir, "restaurant-faiss")

loader = TextLoader(f'{current_dir}/restaurant.txt')

documents = loader.load()

text_spliter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)

docs = text_spliter.split_documents(documents)

