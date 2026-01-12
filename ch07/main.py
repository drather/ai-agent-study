from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

loader = PyPDFLoader("unsu.pdf")
pages = loader.load_and_split()

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False
)

embeddings_model = OpenAIEmbeddings(
    model="text-embeddings-3-large",
    # With the 'text-embedding-3' class
    # of the models, you can specify the size of the embeddings you want returned.
    dimensions=1024
)


