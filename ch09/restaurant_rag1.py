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
