import streamlit as st
import base64

def create_download_button(content, filename):
    b64 = base64.b64encode(content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="color: #fff; background-color: #2E3B55; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-family: Times New Roman;">💾 Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)
