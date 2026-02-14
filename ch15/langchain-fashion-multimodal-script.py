import os
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from datasets import load_dataset
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 이미지를 임베딩해서 크로마디비에 저장하고, 사용자의 문의와의 유사도를 측정
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def setup_dataset():
    dataset = load_dataset("detection-datasets/fashionpedia")

    dataset_folder = os.path.join(SCRIPT_DIR, "fashion-dataset")

    os.makedirs(dataset_folder, exist_ok=True)

def save_images(dataset, dataset_folder, num_images=500):
    for i in range(num_images):
        image = dataset['train'][i]['image']
        image.save(os.path.join(dataset_folder, f'image_{i+1}.png'))
    print(f"saved {num_images} images to {dataset_folder}")


