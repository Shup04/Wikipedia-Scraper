from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 100

def generateGPTResponse(message):
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "system", "content": "You are to summarise fish information into a digestible format for a mobile app in one consice paragraph."},
            {"role": "user", "content": message},
        ],
        temperature=0.3,
    )
    return response

