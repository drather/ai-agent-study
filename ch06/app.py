# https://github.com/sw-woo/hanbit-langchain/

import streamlit as st
from langchain_classic.prompts import PromptTemplate

from langchain_community.llms.ctransformers import CTransformers
from langchain_ollama.llms import OllamaLLM


def getLLMResponse(form_input, email_sender, email_recipient, language) :
    # llm = CTransformers(model='./ch06/llama-2-7b-chat.ggmlv3.q8_0.bin',
    #                     model_type='llama',
    #                     config={'max_new_tokens': 512,
    #                             'temperature': 0.01})

    llm = OllamaLLM(model="llama3.1:8b", temperature=0.7)

    if language == "한국어":
        template = f"""
            {form_input} 주제를 포함한 이메일을 작성해주세요. \n\n 보낸사람: {email_sender} \n 받는사람: {email_recipient} 전부 {language} 로 번역해서 작성해주세요 . 한문은 내용에서 제와해주세요. \n\n 이메일 내용: 
        """
    else:
        template = f"""
            write an email including the topic {form_input}. \n\n Sender: {email_sender }\n Recipient: {email_recipient} Please write the entire email in {language}. \n\n Email content: 
        """

    prompt = PromptTemplate(
        input_variables=["email_topic", "sender", "recipient", "language"],
        template=template
    )

    response = llm.invoke(prompt.format(email_topic=form_input, sender=email_sender, recipient=email_recipient, language=language))
    print(response)

    return response


if __name__ == "__main__":
    st.set_page_config(
        page_title="이메일 생성기 ✉️",
        page_icon=' ✉️',
        layout='centered',
        initial_sidebar_state='collapsed'
    )

    st.header("이메일 생성기 ✉️")

    language_choice = st.selectbox('이메일을 작성할 언어를 선택하세요: ', ['한국어', 'English'])

    form_input = st.text_area('이메일 주제를 입력하세요', height=100)

    col1, col2 = st.columns([10, 10])
    with col1:
        email_sender = st.text_input ('보낸사람 이름')
    with col2:
        email_recipient = st.text_input('받는사람 이름')
    submit = st.button("생성하기")

    if submit:
        with st.spinner('생성중입니다 ...'):
            response = getLLMResponse(form_input, email_sender, email_recipient, language_choice)
            st.write(response)
