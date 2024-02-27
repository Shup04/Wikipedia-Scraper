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
            {"role": "system", "content": "You are to summarize the following information about a specific fish species in a concise paragraph, i will use this fish description in my mobile app."},
            {"role": "user", "content": message},
        ],
        temperature=0,
    )
    return response

