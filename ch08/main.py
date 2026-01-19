from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


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