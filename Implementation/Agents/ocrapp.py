from openai import OpenAI
from pdf2image import convert_from_bytes
from io import BytesIO
import base64
import time
import streamlit as st
from PIL import Image

# Load your OpenAI API key securely
client = OpenAI(api_key=st.secrets["api_keys"]["openai"])

def image_to_base64(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def extract_text_with_gpt4o(image: Image.Image) -> str:
    base64_image = image_to_base64(image)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all readable text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}",
                            "detail": "high"
                        },
                    },
                ],
            }
        ],
        max_tokens=2000,
        temperature=0,
    )

    return response.choices[0].message.content

def extract_pdf_text_with_gpt4o(pdf_bytes: bytes) -> str:
    images = convert_from_bytes(pdf_bytes, dpi=150)
    all_text = []

    for i, img in enumerate(images):
        print(f"🔍 Processing page {i + 1}...")
        try:
            page_text = extract_text_with_gpt4o(img)
            all_text.append(page_text)
            time.sleep(1.1)  # small delay to respect rate limits
        except Exception as e:
            all_text.append(f"[❌ Error on page {i + 1}]: {e}")

    return "\n\n".join(all_text)
