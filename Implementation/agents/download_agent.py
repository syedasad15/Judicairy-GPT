# download_agent.py
import streamlit as st
import io

DOWNLOADABLE_COMMANDS = {
     "generate_legal_judgment": "Legal_Judgment.txt",
    "Research Laws": "Legal_Research_Memo.txt",
    "Draft Legal Briefs": "Draft_Legal_Brief.txt",
    "Review Memo": "Internal_Review_Memo.txt",
    "Draft Judgment": "Draft_Judgment.txt",
    "Format Orders": "Formatted_Order.txt",
    "Proofread Drafts": "Proofread_Document.txt",
    "Type Orders/Letters": "Typed_Legal_Document.txt",
    "Format Order": "Officially_Formatted_Order.txt"
}

def show_download_if_applicable(idx, chats, intent_func):
    if idx == 0:
        print(f"[DEBUG] Skipping idx={idx} (first message)")  # Debug
        return

    print(f"[DEBUG] Processing idx={idx}, chats length={len(chats)}")  # Debug
    user_msg = chats[idx - 1]["message"]
    intent = intent_func(user_msg)
    print(f"[DEBUG] User message: {user_msg}, Intent: {intent}")  # Debug

    if intent in DOWNLOADABLE_COMMANDS:
        print(f"[DEBUG] Intent {intent} is downloadable")  # Debug
        data = chats[idx]["message"]
        if any(keyword in user_msg.lower() for keyword in ["petition", "draft petition", "generate petition"]):
            filename = "petition.txt"
            print(f"[DEBUG] Petition keyword detected, filename: {filename}")  # Debug
        else:
            filename = f"{intent.replace(' ', '_').lower()}.txt"
            print(f"[DEBUG] Filename: {filename}")  # Debug

        st.download_button(
            label="📥 Download Response",
            data=data,
            file_name=filename,
            mime="text/plain",
            key=f"download_{idx}"
        )
    else:
        print(f"[DEBUG] Intent {intent} not in DOWNLOADABLE_COMMANDS")  # Debug