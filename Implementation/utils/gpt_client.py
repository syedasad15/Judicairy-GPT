# utils/gpt_client.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("key.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt4(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
