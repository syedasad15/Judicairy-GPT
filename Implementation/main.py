
# import streamlit as st
# from prompt_router import handle_user_input, generate_title_from_prompt

# import uuid
# import os
# from Agents import download_agent,ocrapp
# from utils import intent_classifier 
# from Agents.title_generator import generate_chat_title

# st.set_page_config(page_title="PakLaw Judicial Assistant", layout="wide")

# # --- Session State Initialization ---
# if "chats" not in st.session_state:
#     st.session_state.chats = {}
# if "chat_titles" not in st.session_state:
#     st.session_state.chat_titles = {}
# if "current_chat" not in st.session_state:
#     chat_id = str(uuid.uuid4())
#     st.session_state.current_chat = chat_id
#     st.session_state.chats[chat_id] = []
#     st.session_state.chat_titles[chat_id] = "New Chat"
# if "user_input" not in st.session_state:
#     st.session_state.user_input = ""
# if "uploaded_case_text" not in st.session_state:
#     st.session_state.uploaded_case_text = ""

# # --- Sidebar Chat Management ---
# st.sidebar.title("💬 Case Files")
# if st.sidebar.button("➕ New Case"):
#     chat_id = str(uuid.uuid4())
#     st.session_state.current_chat = chat_id
#     st.session_state.chats[chat_id] = []
#     st.session_state.chat_titles[chat_id] = "New Case"
#     st.session_state.uploaded_case_text = ""

# for cid in st.session_state.chats:
#     title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
#     if st.sidebar.button(title, key=cid):
#         st.session_state.current_chat = cid

# # --- Title ---
# st.title("⚖️ PakLaw Judicial Assistant")
# st.markdown("This assistant provides support for tasks within Pakistan's judicial system.")

# # --- Top Section: Display Chat History with HTML Styling ---
# def format_response_to_html(text):
#     import re
#     text = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\1:</strong>", text)
#     text = text.replace("\n", "<br>")
#     return text

# with st.container():
#     st.markdown("### 📜 Case Discussion & Judgments")

#     current_chat = st.session_state.chats[st.session_state.current_chat]

#     for idx, msg in enumerate(current_chat):
#         if msg["role"] == "user":
#             st.markdown(
#                 f"""
#                 <div style='padding: 10px; background-color: #e6f0fa;
#                     border-left: 4px solid #007acc; border-radius: 6px;
#                     margin-bottom: 10px;'>
#                     <strong>🧑 Counsel:</strong><br>{msg['message']}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
                
#             )

#         elif msg["role"] == "assistant":
#             formatted_response = format_response_to_html(msg["message"])
#             st.markdown(
#                 f"""
#                 <div style='padding: 10px; background-color: #f6f8fa;
#                     border-left: 4px solid #2E3B55; border-radius: 6px;
#                     margin-bottom: 10px;'>
#                     <strong>⚖️ Assistant:</strong><br>{formatted_response}
#                 </div>
#                 """,
#                 unsafe_allow_html=True
#             )

#             # 🧠 Show download button only for matching prompts
#             print(f"[DEBUG] Calling show_download_if_applicable for idx={idx}")  # Debug
#             download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)


# # --- Sticky Input Box at Bottom ---
# st.markdown(
#     """
#     <style>
#     .chat-input-wrapper {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         right: 0;
#         padding: 1rem 3rem 1.5rem 3rem;
#         background-color: #ffffff;
#         border-top: 2px solid #2E3B55;
#         box-shadow: 0 -2px 6px rgba(0,0,0,0.05);
#         z-index: 100;
#     }
#     .stTextArea textarea {
#         background-color: #ffffff !important;
#         border: 2px solid #2E3B55 !important;
#         border-radius: 10px !important;
#         padding: 1rem !important;
#         font-size: 1.1rem !important;
#         color: #1A252F !important;
#         resize: none !important;
#         font-family: 'Times New Roman', Times, serif;
#     }
#     .stTextArea textarea:focus {
#         border-color: #FFD700 !important;
#         outline: none !important;
#         box-shadow: 0 0 6px rgba(255, 215, 0, 0.3) !important;
#     }
#     .stButton>button {
#         border-radius: 8px !important;
#         font-family: 'Times New Roman', Times, serif;
#         padding: 0.5rem 1.5rem !important;
#     }
#     </style>
#     <div class='chat-input-wrapper'>
#     """,
#     unsafe_allow_html=True
# )
# from Agents.ocrapp import extract_pdf_text  # updated function

# with st.form(key="chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([4, 1])

#     with col1:
#         user_input = st.text_area(
#             "Enter your judicial query:",
#             key="user_input",
#             label_visibility="collapsed",
#             height=100,
#             placeholder="Type your legal query here or upload a .txt or .pdf case..."
#         )

#         uploaded_file = st.file_uploader(
#             "📎 Upload Case File (.txt or .pdf)",
#             type=["txt", "pdf"],
#             label_visibility="collapsed"
#         )

#         if uploaded_file:
#             file_name = uploaded_file.name.lower()

#             if file_name.endswith(".txt"):
#                 st.session_state.uploaded_case_text = uploaded_file.read().decode("utf-8")
#                 st.success("✅ Text file loaded successfully.")

#             elif file_name.endswith(".pdf"):
#                 with st.spinner("🔍 Extracting text from PDF..."):
#                     extracted_text = extract_pdf_text(uploaded_file.read())
#                     st.session_state.uploaded_case_text = extracted_text
#                 st.success("✅ PDF processed and text extracted!")

#             else:
#                 st.warning("❌ Only .txt and .pdf files are supported.")

#     with col2:
#         submitted = st.form_submit_button("Submit Query")

# # --- Handle Query ---
# if submitted and (user_input or st.session_state.uploaded_case_text):
#     query = user_input.strip() or "Generate legal judgment"

#     with st.spinner("Processing..."):
#         response = handle_user_input(query)

#     chat_id = st.session_state.current_chat
#     if uploaded_file:
#         st.session_state.chats[chat_id].append({"role": "user", "message": f"[📎 Uploaded Case File: {uploaded_file.name}]"})

#     st.session_state.chats[chat_id].append({"role": "user", "message": query})
#     st.session_state.chats[chat_id].append({"role": "assistant", "message": response})

   

#     title = generate_chat_title(query)
#     st.session_state.chat_titles[chat_id] = title if title else "Untitled Case"


#     st.rerun()










import streamlit as st
from prompt_router import handle_user_input, generate_title_from_prompt
import uuid
import os
from Agents import download_agent, ocrapp
from utils import intent_classifier 
from Agents.title_generator import generate_chat_title

# Set page configuration
st.set_page_config(page_title="PakLaw Judicial Assistant", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Enhanced UI ---
st.markdown("""
    <style>
    /* General Styling */
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #F6F8FA;
        color: #1A252F;
    }
    h1, h2, h3 {
        font-family: 'Roboto Slab', serif;
        color: #2E3B55;
    }
    .stSidebar {
        background-color: #2E3B55;
        color: #F6F8FA;
        padding: 1rem;
    }
    .stSidebar button {
        background-color: #FFD700;
        color: #1A252F;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        margin: 0.2rem 0;
        width: 100%;
        text-align: left;
        transition: transform 0.2s;
    }
    .stSidebar button:hover {
        transform: scale(1.02);
        background-color: #FFCA28;
    }
    .chat-container {
        max-height: 60vh;
        overflow-y: auto;
        padding: 1rem;
        margin-bottom: 120px; /* Space for sticky input */
    }
    .chat-message {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        line-height: 1.5;
    }
    .user-message {
        background-color: #E6F0FA;
        border-left: 4px solid #007ACC;
    }
    .assistant-message {
        background-color: #FFFFFF;
        border-left: 4px solid #2E3B55;
    }
    .chat-input-wrapper {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1rem;
        background-color: #FFFFFF;
        border-top: 2px solid #2E3B55;
        box-shadow: 0 -2px 6px rgba(0,0,0,0.05);
        z-index: 100;
    }
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 2px solid #2E3B55 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        font-size: 16px !important;
        color: #1A252F !important;
        resize: none !important;
    }
    .stTextArea textarea:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 6px rgba(255, 215, 0, 0.3) !important;
    }
    .stButton>button {
        background-color: #FFD700;
        color: #1A252F;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        background-color: #FFCA28;
    }
    .stFileUploader {
        border: 2px dashed #2E3B55;
        border-radius: 8px;
        padding: 0.5rem;
    }
    /* Responsive Design */
    @media (max-width: 768px) {
        .stSidebar {
            position: fixed;
            z-index: 200;
            width: 80%;
            height: 100%;
            transition: transform 0.3s;
        }
        .stSidebar[aria-expanded="false"] {
            transform: translateX(-100%);
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = {}
if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.chats[chat_id] = []
    st.session_state.chat_titles[chat_id] = "New Case"
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "uploaded_case_text" not in st.session_state:
    st.session_state.uploaded_case_text = ""

# --- Sidebar Chat Management ---
with st.sidebar:
    st.markdown("<h2 style='color: #F6F8FA;'>💬 Case Files</h2>", unsafe_allow_html=True)
    
    # Search bar for chat history
    search_query = st.text_input("Search Cases", placeholder="Enter case title...", label_visibility="collapsed")
    
    # New Case Button
    if st.button("➕ New Case", key="new_case"):
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = []
        st.session_state.chat_titles[chat_id] = "New Case"
        st.session_state.uploaded_case_text = ""
        st.rerun()
    
    # Chat List
    for cid in st.session_state.chats:
        title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
        if search_query.lower() in title.lower():
            if st.button(title, key=cid):
                st.session_state.current_chat = cid
                st.rerun()

# --- Main Content ---
st.markdown("<h1 style='text-align: center;'>⚖️ PakLaw Judicial Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #1A252F;'>Your AI-powered assistant for Pakistan's judicial system</p>", unsafe_allow_html=True)

# --- Chat History ---
with st.container():
    st.markdown("<h3>📜 Case Discussion & Judgments</h3>", unsafe_allow_html=True)
    chat_container = st.container()
    with chat_container:
        current_chat = st.session_state.chats[st.session_state.current_chat]
        for idx, msg in enumerate(current_chat):
            timestamp = "Just now"  # Replace with actual timestamp logic if needed
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class='chat-message user-message'>
                        <strong>🧑 Counsel:</strong> {msg['message']}<br>
                        <small style='color: #6B7280;'>{timestamp}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif msg["role"] == "assistant":
                formatted_response = msg["message"].replace("\n", "<br>")
                st.markdown(
                    f"""
                    <div class='chat-message assistant-message'>
                        <strong>⚖️ Assistant:</strong> {formatted_response}<br>
                        <small style='color: #6B7280;'>{timestamp}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# --- Sticky Input Box ---
with st.container():
    st.markdown("<div class='chat-input-wrapper'>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_area(
                "Enter your judicial query:",
                key="user_input",
                label_visibility="collapsed",
                height=100,
                placeholder="Type your legal query or upload a case file (.txt or .pdf)..."
            )
            uploaded_file = st.file_uploader(
                "📎 Upload Case File (.txt or .pdf)",
                type=["txt", "pdf"],
                label_visibility="collapsed"
            )
            if uploaded_file:
                file_name = uploaded_file.name.lower()
                if file_name.endswith(".txt"):
                    st.session_state.uploaded_case_text = uploaded_file.read().decode("utf-8")
                    st.success("✅ Text file loaded successfully.")
                elif file_name.endswith(".pdf"):
                    with st.spinner("🔍 Extracting text from PDF..."):
                        extracted_text = ocrapp.extract_pdf_text(uploaded_file.read())
                        st.session_state.uploaded_case_text = extracted_text
                    st.success("✅ PDF processed and text extracted!")
                else:
                    st.warning("❌ Only .txt and .pdf files are supported.")
        with col2:
            col_submit, col_clear = st.columns(2)
            with col_submit:
                submitted = st.form_submit_button("Submit", use_container_width=True)
            with col_clear:
                if st.form_submit_button("Clear", use_container_width=True):
                    st.session_state.user_input = ""
                    st.session_state.uploaded_case_text = ""
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# --- Handle Query ---
if submitted and (user_input or st.session_state.uploaded_case_text):
    query = user_input.strip() or "Generate legal judgment"
    with st.spinner("⚖️ Processing your query..."):
        response = handle_user_input(query)
    
    chat_id = st.session_state.current_chat
    if uploaded_file:
        st.session_state.chats[chat_id].append({"role": "user", "message": f"[📎 Uploaded Case File: {uploaded_file.name}]"})
    
    st.session_state.chats[chat_id].append({"role": "user", "message": query})
    st.session_state.chats[chat_id].append({"role": "assistant", "message": response})
    
    title = generate_chat_title(query)
    st.session_state.chat_titles[chat_id] = title if title else "Untitled Case"
    
    st.rerun()
