from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

loader = PyPDFLoader("unsu.pdf")
pages = loader.load_and_split()

text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False
)

texts = text_spliter.split_documents(pages)

embeddings_model = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the 'text-embedding-3' class
    # of the models, you can specify the size of the embeddings you want returned.
    dimensions=1024
)

db = Chroma.from_documents(texts, embeddings_model)

question = "아내가 먹고 싶어하는 음식은 뭐야?"
llm = ChatOpenAI(temperature=0)

retriever_from_llm = MultiQueryRetriever.from_llm(retriever=db.as_retriever(), llm=llm)

docs = retriever_from_llm.invoke(question)
print(len(docs))

for doc in docs:
    print(doc)
