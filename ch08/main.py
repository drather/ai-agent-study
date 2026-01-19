import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

st.header("현진건 작가님과의 대화")

# 대화 히스토리 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 질문 입력
prompt = st.chat_input("물어보고 싶은 것을 입력하세요!")
if prompt:
    st.write(f"user has sent the follwing prompt: {prompt}")
    with st.chat_message('user'):
        st.write(prompt)
        st.session_state.chat_history.append({'role': 'user', 'content': prompt})

response = client.responses.create(
    model="gpt-4o-mini",
    input="아내가 먹고싶어한 음식이 뭐야?",
    instructions="당신은 소설 운수좋은날을 집필한 현진건 작가님입니다",
    tools=[{
        "type":"file_search",
        "vector_store_ids": ["vs_696e2e17a40c819180a4ad39b6606b67"]
    }]
)

print(response.output_text)


second_response = client.responses.create(
    previous_response_id=response.id,
    model="gpt-4o-mini",
    instructions="당신은 소설 운수좋은날을 집필한 현진건 작가님입니다",
    input="방금 뭐라고했어?",
    tools=[{
        "type":"file_search",
        "vector_store_ids": ["vs_696e2e17a40c819180a4ad39b6606b67"]
    }]
)

print(second_response.output_text)