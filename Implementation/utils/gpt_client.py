import streamlit as st
import os
from openai import OpenAI

client = openai_api_key = st.secrets["api_keys"]["openai"]

def call_gpt4(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
