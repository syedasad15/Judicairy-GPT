# import streamlit as st
# from prompt_router import handle_user_input, generate_title_from_prompt

# import uuid
# import os
# from Agents import download_agent
# from utils import intent_classifier
# from Agents.title_generator import generate_chat_title
# from Agents.ocrapp import extract_pdf_text_with_vision
# import hashlib

# # --- Page Setup ---
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
# if "last_uploaded_file_hash" not in st.session_state:
#     st.session_state.last_uploaded_file_hash = None

# # --- Sidebar Chat Management ---
# st.sidebar.title("💬 Case Files")
# if st.sidebar.button("➕ New Case"):
#     chat_id = str(uuid.uuid4())
#     st.session_state.current_chat = chat_id
#     st.session_state.chats[chat_id] = []
#     st.session_state.chat_titles[chat_id] = "New Case"
#     st.session_state.uploaded_case_text = ""
#     st.session_state.last_uploaded_file_hash = None

# for cid in st.session_state.chats:
#     title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
#     if st.sidebar.button(title, key=cid):
#         st.session_state.current_chat = cid

# # --- Title and Description ---
# st.title("⚖️ PakLaw Judicial Assistant")
# st.markdown("This assistant provides support for tasks within Pakistan's judicial system.")

# # --- Chat History Display ---
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
#             download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# # --- Sticky Chat Input Style ---
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

# # --- Input Form ---
# with st.form(key="chat_form", clear_on_submit=True):
#     col1, col2 = st.columns([4, 1])

#     file_valid = True
#     file_error_message = ""

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

#         max_file_size_mb = 10

#         if uploaded_file:
#             file_name = uploaded_file.name.lower()
#             file_bytes = uploaded_file.read()
#             file_hash = hashlib.md5(file_bytes).hexdigest()

#             if uploaded_file.size > max_file_size_mb * 1024 * 1024:
#                 file_valid = False
#                 file_error_message = f"❌ File is too large. Max allowed size is {max_file_size_mb} MB."
#                 st.session_state.uploaded_case_text = ""
#                 st.session_state.last_uploaded_file_hash = None
#                 st.error(file_error_message)

#             elif st.session_state.last_uploaded_file_hash != file_hash:
#                 try:
#                     if file_name.endswith(".txt"):
#                         st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
#                         st.success("✅ Text file loaded successfully.")

#                     elif file_name.endswith(".pdf"):
#                         extracted_text = extract_pdf_text_with_vision(file_bytes)
#                         st.session_state.uploaded_case_text = extracted_text
#                         st.success("✅ PDF processed and text extracted!")

#                     st.session_state.last_uploaded_file_hash = file_hash

#                 except Exception as e:
#                     file_valid = False
#                     file_error_message = f"❌ Failed to extract text: {e}"
#                     st.session_state.uploaded_case_text = ""
#                     st.session_state.last_uploaded_file_hash = None
#                     st.error(file_error_message)

#     with col2:
#         submitted = st.form_submit_button("Submit Query")

# # --- Handle Query ---
# if submitted:
#     if uploaded_file and not file_valid:
#         st.error("❌ Cannot submit. Uploaded file is either too large or invalid.")
#     elif not user_input.strip() and not st.session_state.uploaded_case_text:
#         st.warning("⚠️ Please enter a query or upload a valid case file.")
#     else:
#         query = user_input.strip() or "Generate legal judgment"

#         with st.spinner("Processing..."):
#             response = handle_user_input(query)

#         chat_id = st.session_state.current_chat

#         if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
#             st.session_state.chats[chat_id].append({
#                 "role": "user",
#                 "message": f"[📎 Uploaded Case File: {uploaded_file.name}]"
#             })

#         st.session_state.chats[chat_id].append({
#             "role": "user",
#             "message": query
#         })

#         st.session_state.chats[chat_id].append({
#             "role": "assistant",
#             "message": response
#         })

#         title = generate_chat_title(query)
#         st.session_state.chat_titles[chat_id] = title if title else "Untitled Case"
#         st.rerun()



# import streamlit as st
# from prompt_router import handle_user_input, generate_title_from_prompt
# from PyPDF2 import PdfReader
# from io import BytesIO
# import uuid
# import os
# from Agents import download_agent
# from utils import intent_classifier
# from Agents.title_generator import generate_chat_title
# from Agents.ocrapp import extract_pdf_text_with_vision
# import hashlib

# # --- Page Setup ---
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
# if "last_uploaded_file_hash" not in st.session_state:
#     st.session_state.last_uploaded_file_hash = None

# # --- Sidebar Chat Management ---
# st.sidebar.title("💬 Case Files")
# if st.sidebar.button("➕ New Case"):
#     chat_id = str(uuid.uuid4())
#     st.session_state.current_chat = chat_id
#     st.session_state.chats[chat_id] = []
#     st.session_state.chat_titles[chat_id] = "New Case"
#     st.session_state.uploaded_case_text = ""
#     st.session_state.last_uploaded_file_hash = None

# for cid in st.session_state.chats:
#     title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
#     if st.sidebar.button(title, key=cid):
#         st.session_state.current_chat = cid

# # --- Title and Description ---
# st.title("⚖️ PakLaw Judicial Assistant")
# st.markdown("This assistant provides support for tasks within Pakistan's judicial system.")

# # --- Chat History Display ---
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
#             download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# # --- Sticky Chat Input Style ---
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

# # --- Input Form ---
# file_valid = True
# file_error_message = ""

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

#         st.markdown(
#     "<small style='color: #666;'>Limit: 10MB per file • Max 30 pages • TXT, PDF</small>",
#     unsafe_allow_html=True
# )

#         uploaded_file = st.file_uploader(
#             "📎 Upload Case File (.txt or .pdf)",
#             type=["txt", "pdf"],
#             label_visibility="collapsed"
#         )


        

#         if uploaded_file:
#             max_file_size_mb = 10
#             if uploaded_file.size > max_file_size_mb * 1024 * 1024:
#                 file_valid = False
#                 file_error_message = f"❌ File is too large. Max allowed size is {max_file_size_mb} MB."
#                 st.error(file_error_message)
#             else:
#                 file_name = uploaded_file.name.lower()
#                 file_bytes = uploaded_file.read()
#                 file_hash = hashlib.md5(file_bytes).hexdigest()

#                 if st.session_state.last_uploaded_file_hash != file_hash:
#                     st.session_state.last_uploaded_file_hash = file_hash
#                     try:
#                         if file_name.endswith(".txt"):
#                             st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
#                             st.success("✅ Text file loaded successfully.")

#                         elif file_name.endswith(".pdf"):
#                             try:
#                                 reader = PdfReader(BytesIO(file_bytes))
#                                 page_count = len(reader.pages)
                        
#                                 if page_count > 30:
#                                     file_valid = False
#                                     file_error_message = "❌ PDF too long. Max 30 pages allowed."
#                                     st.error(file_error_message)
#                                 else:
#                                     extracted_text = extract_pdf_text_with_vision(file_bytes)
                        
#                                     if not extracted_text or len(extracted_text.strip()) < 50:
#                                         file_valid = False
#                                         file_error_message = "❌ PDF was processed but no meaningful text was extracted."
#                                         st.error(file_error_message)
#                                     else:
#                                         st.session_state.uploaded_case_text = extracted_text[:10000]  # Optional truncation
#                                         st.success("✅ PDF processed and text extracted!")
                        
#                             except Exception as e:
#                                 file_valid = False
#                                 file_error_message = f"❌ Failed to extract text: {str(e)}"
#                                 st.error(file_error_message)


#                     except Exception as e:
#                         file_valid = False
#                         file_error_message = "❌ Invalid or unreadable file. Please upload a valid PDF or TXT file."
#                         st.error(file_error_message)

#     with col2:
#         submitted = st.form_submit_button("Submit Query")

# # --- Additional Submission Check ---
# if submitted:
#     if uploaded_file and not file_valid and not file_error_message:
#         st.error("❌ Cannot submit. Uploaded file is either too large or invalid.")

# # --- Handle Query ---
# if submitted and (user_input or st.session_state.uploaded_case_text) and file_valid:
#     query = user_input.strip() or "Generate legal judgment"

#     with st.spinner("Processing..."):
#         response = handle_user_input(query)

#     chat_id = st.session_state.current_chat

#     if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
#         st.session_state.chats[chat_id].append({
#             "role": "user",
#             "message": f"[📎 Uploaded Case File: {uploaded_file.name}]"
#         })

#     st.session_state.chats[chat_id].append({
#         "role": "user",
#         "message": query
#     })

#     st.session_state.chats[chat_id].append({
#         "role": "assistant",
#         "message": response
#     })

#     title = generate_chat_title(query)
#     st.session_state.chat_titles[chat_id] = title if title else "Untitled Case"
#     st.rerun()

###############################################################################
#  PakLaw Judicial Assistant  –  PREMIUM  UI  FINAL
###############################################################################
import streamlit as st
from prompt_router import handle_user_input
from PyPDF2 import PdfReader
from io import BytesIO
import uuid
import os
from Agents import download_agent
from utils import intent_classifier
from Agents.title_generator import generate_chat_title
from Agents.ocrapp import extract_pdf_text_with_vision
import hashlib
import re

# ---------- Page Config ----------
st.set_page_config(
    page_title="PakLaw Judicial Assistant",
    page_icon="⚖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- Google Fonts ----------
st.markdown(
    """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Serif+Pro:wght@300;400;600&display=swap" rel="stylesheet">
""",
    unsafe_allow_html=True,
)

# ---------- Global CSS ----------
st.markdown(
    """
<style>
:root {
    --charcoal: #111827;
    --charcoal-light: #1f2937;
    --gold: #bfa46f;
    --gold-soft: #d4bc8b;
    --ivory: #fdfcf9;
    --radius: 12px;
    --shadow: 0 2px 10px rgba(0,0,0,.07);
    --shadow-hover: 0 4px 20px rgba(0,0,0,.12);
}

html, body, .main, [data-testid="stApp"] {
    background-color: var(--ivory);
    font-family: 'Source Serif Pro', serif;
    color: var(--charcoal);
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    color: var(--charcoal);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--charcoal);
    border-right: none;
}
.sidebar-card {
    background: var(--charcoal-light);
    color: var(--ivory);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    margin-bottom: .6rem;
    transition: .25s;
    font-family: 'Source Serif Pro', serif;
}
.sidebar-card:hover {
    background: var(--gold);
    color: var(--charcoal);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}

/* Chat bubbles */
.chat-user, .chat-assistant {
    max-width: 80%;
    padding: .9rem 1.2rem;
    border-radius: var(--radius);
    margin-bottom: .8rem;
    animation: fadeIn .4s ease-in-out;
}
.chat-user {
    background: #f3f0eb;
    border-left: 4px solid var(--gold);
    margin-left: auto;
    color: var(--charcoal);
}
.chat-assistant {
    background: #ede8e1;
    border-left: 4px solid var(--charcoal);
    margin-right: auto;
    color: var(--charcoal);
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to   {opacity: 1; transform: translateY(0);}
}

/* Sticky bottom bar */
.chat-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--ivory);
    border-top: 2px solid var(--gold-soft);
    box-shadow: var(--shadow);
    z-index: 1000;
    padding: .9rem 2.2rem 1.4rem;
    font-family: 'Source Serif Pro', serif;
}
.chat-bar textarea {
    border: 2px solid var(--gold);
    border-radius: var(--radius);
    font-size: 1.05rem;
    font-family: 'Source Serif Pro', serif;
}
.chat-bar textarea:focus {
    border-color: var(--charcoal);
    box-shadow: 0 0 0 .15rem rgba(191,164,111,.35);
}
.stButton>button {
    border-radius: var(--radius);
    font-family: 'Playfair Display', serif;
    font-weight: 600;
    background: var(--gold);
    color: var(--charcoal);
    border: none;
    transition: .25s;
}
.stButton>button:hover {
    background: var(--gold-soft);
    transform: translateY(-1px);
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Session State ----------
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "chat_titles" not in st.session_state:
    st.session_state.chat_titles = {}
if "current_chat" not in st.session_state:
    cid = str(uuid.uuid4())
    st.session_state.current_chat = cid
    st.session_state.chats[cid] = []
    st.session_state.chat_titles[cid] = "New Case"
if "uploaded_case_text" not in st.session_state:
    st.session_state.uploaded_case_text = ""
if "last_uploaded_file_hash" not in st.session_state:
    st.session_state.last_uploaded_file_hash = None

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("### 📁 Case Files")
    if st.button("➕ New Case", use_container_width=True):
        cid = str(uuid.uuid4())
        st.session_state.current_chat = cid
        st.session_state.chats[cid] = []
        st.session_state.chat_titles[cid] = "New Case"
        st.session_state.uploaded_case_text = ""
        st.session_state.last_uploaded_file_hash = None
        st.rerun()

    for cid in list(st.session_state.chats.keys()):
        title = st.session_state.chat_titles.get(cid, f"Case {cid[:8]}")
        if st.button(title, key=f"chat_{cid}", use_container_width=True):
            st.session_state.current_chat = cid
            st.rerun()

# ---------- Main Area ----------
st.title("⚖ PakLaw Judicial Assistant")
st.caption("Interactive legal assistant for Pakistan’s judicial system.")

st.markdown("### 📜 Case Discussion & Judgments")

chat_id = st.session_state.current_chat
current_chat = st.session_state.chats[chat_id]

chat_area = st.container()
with chat_area:
    for idx, msg in enumerate(current_chat):
        if msg["role"] == "user":
            st.markdown(
                f'<div class="chat-user"><strong>🧑 Counsel:</strong><br>{msg["message"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            html = re.sub(r"(?m)^([A-Z][a-z]+):", r"<strong>\1:</strong>", msg["message"])
            html = html.replace("\n", "<br>")
            st.markdown(
                f'<div class="chat-assistant"><strong>⚖ Assistant:</strong><br>{html}</div>',
                unsafe_allow_html=True,
            )
            download_agent.show_download_if_applicable(idx, current_chat, intent_classifier.classify_prompt_intent)

# ---------- Sticky Input ----------
with st.container():
    st.markdown('<div class="chat-bar">', unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        c1, c2 = st.columns([4, 1])

        with c1:
            user_input = st.text_area(
                "Enter your judicial query:",
                key="user_input",
                label_visibility="collapsed",
                height=100,
                placeholder="Type your legal query here or upload a .txt / .pdf case …"
            )

            uploaded_file = st.file_uploader(
                "📎 Upload Case File (.txt or .pdf)",
                type=["txt", "pdf"],
                label_visibility="collapsed",
            )
            st.caption(
                "<small style='color:#666;'>Limit: 10 MB • Max 30 pages • TXT, PDF</small>",
                unsafe_allow_html=True,
            )

            if uploaded_file:
                max_mb = 10
                if uploaded_file.size > max_mb * 1024 * 1024:
                    st.error(f"❌ File too large. Max {max_mb} MB allowed.")
                else:
                    file_bytes = uploaded_file.read()
                    file_hash = hashlib.md5(file_bytes).hexdigest()
                    if st.session_state.last_uploaded_file_hash != file_hash:
                        st.session_state.last_uploaded_file_hash = file_hash
                        try:
                            if uploaded_file.name.lower().endswith(".txt"):
                                st.session_state.uploaded_case_text = file_bytes.decode("utf-8")
                                st.success("✅ Text file loaded.")
                            else:
                                reader = PdfReader(BytesIO(file_bytes))
                                if len(reader.pages) > 30:
                                    st.error("❌ PDF too long. Max 30 pages.")
                                else:
                                    txt = extract_pdf_text_with_vision(file_bytes)
                                    if not txt or len(txt.strip()) < 50:
                                        st.error("❌ No meaningful text extracted.")
                                    else:
                                        st.session_state.uploaded_case_text = txt[:10_000]
                                        st.success("✅ PDF processed.")
                        except Exception as e:
                            st.error(f"❌ Could not read file: {e}")

        with c2:
            submitted = st.form_submit_button("Submit", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------- Query Handler ----------
if submitted and (user_input or st.session_state.uploaded_case_text):
    query = user_input.strip() or "Generate legal judgment"
    with st.spinner("Processing …"):
        response = handle_user_input(query)

    if uploaded_file and uploaded_file.size <= 10 * 1024 * 1024:
        current_chat.append({"role": "user", "message": f"[📎 Uploaded: {uploaded_file.name}]"})

    current_chat.append({"role": "user", "message": query})
    current_chat.append({"role": "assistant", "message": response})

    st.session_state.chat_titles[chat_id] = generate_chat_title(query) or "Untitled Case"
    st.rerun()





