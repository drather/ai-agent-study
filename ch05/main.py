from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

llm = init_chat_model("gpt-4o-mini", model_provider="openai")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])
output_parser = StrOutputParser()

chain = prompt | llm | output_parser

content = "코딩"

result = chain.invoke({"input": content + " 에 대한 시를 써줘"})
print (result)

st.title("This is a title")
st.title('_Streamlit_ is :blue[cool] :sunglasses:')

