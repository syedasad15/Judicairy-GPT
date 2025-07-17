import streamlit as st
import os
from openai import OpenAI


# Get the API key from Streamlit secrets
openai_api_key = st.secrets["api_keys"]["openai"]

# Properly initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

def call_gpt4(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()
