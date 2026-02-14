import base64
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


def setup_chroma_db():
    vdb_path = os.path.join(SCRIPT_DIR, "img_vdb")

    chroma_client = chromadb.PersistentClient(path=vdb_path)

    image_loader = ImageLoader()

    CLIP = OpenCLIPEmbeddingFunction()

    image_vdb = chroma_client.get_or_create_collention(name="image", embedding_function=CLIP, data_loader=image_loader)
    return image_vdb

def add_images_to_db(image_vdb, dataset_folder) :
    ids = []
    uris = []

    for i, filename in enumerate(sorted(os.listdir(dataset_folder))):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            file_path = os.path.join(dataset_folder, filename)
            ids.append(str(i))
            uris.append(file_path)
        image_vdb.add(ids=ids, uris=uris)
        print("이미지가 데이터베이스에 추가되었습니다.")

def query_db(image_vdb, query, results=2):
    return image_vdb.query(
        query_texts=[query],
        n_results=results,
        includ=['uris', 'distances']
    )

def print_results(results):
    for idx, uri in enumerate(results['uris'][0]):
        print(f"ID: {results['ids'][0][idx]}")
        print(f"Distances: {results['distances'][0][idx]}")
        print(f"Path: {uri}")
        print("\n")

def translate(text, target_lang):
    translation_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0)

    translation_prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a translator. Translate the following text: {text} to {target_lang}", ),
        ("user", "{text")
    ])

    translation_chain = translation_prompt | translation_model | StrOutputParser()

    return translation_chain.invoke({"text": text})

def setup_vision_chain():
    # GPT-4 모델을 사용하여 시각적 정보를 처리 gpt-4o or gpt-4o-mini 모델선택
    gpt4 = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    parser = StrOutputParser()

    # 당신은 유용한 패션 및 스타일링 보조자입니다. 제공된 이미지 부분을 직접 참조하여 주어진 이미지 컨텍스트를 사용하여 사용자의 질문에 답합니다. 좀 더 대화적인 분위기를 유지하고 목록을 너무 많이 만들지 마십시오. 하이라이트, 강조, 구조를 위해 마크다운 형식을 사용하세요.
    image_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful fashion and styling assistant. Answer the user's question using the given image context with direct references to parts of the images provided. Maintain a more conversational tone, don't make too many lists. Use markdown formatting for highlights, emphasis, and structure."),
        ("user", [
            {"type": "text", "text": "What are some ideas for styling {user_query}"},
            {"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data_1}"},
            {"type": "image_url", "image_url": "data:image/jpeg;base64,{image_data_2}"},
        ]),
    ])
    # 프롬프트, 모델, 파서 체인을 반환
    return image_prompt | gpt4 | parser


def format_prompt_inputs(data, user_query):
    inputs = {}

    inputs['user_query'] = user_query

    image_path_1 = data['uris'][0][1]
    image_path_2 = data['uris'][0][2]

    with open(image_path_1, 'rb') as image_file:
        image_data_1 = image_file.read()
    inputs['image_data_1'] = base64.b64encode(image_data_1).decode('utf-8')

    with open(image_path_2, 'rb') as image_file:
        image_data_2 = image_file.read()
    inputs['image_data_2'] = base64.b64encode(image_data_2).decode('utf-8')
    return inputs
