from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from langchain_openai import ChatOpenAI

from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
print(OPENAI_API_KEY)

openai = ChatOpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY, temperature=0.7)

prompt1 = PromptTemplate.from_template( "다음 식당 리뷰를 한 문장으로 요약하세요 \n\n {review}")

chain1 = LLMChain(llm=openai, prompt=prompt1, output_key="summary")
prompt2 = PromptTemplate.from_template("다음 식당 리뷰를 읽고 0점부터 10점 사이에서 긍정/부정 점수를 매기세요. 숫자로만 대답하세요 \n\n{review}")

chain2 = LLMChain(llm=openai, prompt=prompt2, output_key="sentiment_score")

prompt3 = PromptTemplate.from_template("다음 식당 리뷰 요약에 공손한 답변을 작성하세요 \n 리뷰 요약: {summary}")

chain3 = LLMChain(llm=openai, prompt=prompt3, output_key="reply")

all_chain = SequentialChain(
    chains=[chain1, chain2, chain3],
    input_variables=['review'],
    output_variables=['summary', 'sentiment_score', 'reply']
)

review = """
    이식당은 맛도 좋고 분위기도 좋았습니다. 가격대비만족도가 높아요. 
    하지만, 서비스 속도가 너무 느려서 조금 실망스러웠습니다. 
    전반적으로는 다시 방문할 의사가 있습니다. 
"""


# 체인 실행 및 결과 출력
try:
    result = all_chain.invoke(input={'review':review})
    print(f"summary = \n {result["summary"]} \n")
    print(f"sentiment_score = \n {result["sentiment_score"]} \n")
    print(f"reply = \n {result["reply"]} \n")
except Exception as e:
    print(f"error = {e}")

