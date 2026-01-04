from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


load_dotenv(verbose=True)

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assisstant"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
result = chain.invoke({"input": "hi"})
print(result)

