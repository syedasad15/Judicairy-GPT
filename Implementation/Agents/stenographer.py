from utils.gpt_client import call_gpt4

def type_judgments(user_input):
    prompt = f"""
Draft a judgment based on the following summary or instructions. Format it formally for a Pakistani judge.

Details: {user_input}

Include:
- Introduction
- Issue framing
- Arguments
- Reasoning
- Final verdict
"""
    return call_gpt4(prompt)


def format_orders(user_input):
    prompt = f"""
Format the following order into a professional court document for a Pakistani judge.

Order Text: {user_input}

Ensure proper legal structure and formatting is applied.
"""
    return call_gpt4(prompt)


def proofread_drafts(user_input):
    prompt = f"""
Proofread and improve this legal draft for clarity, grammar, and proper judicial tone. It must comply with Pakistani legal format.

Text: {user_input}
"""
    return call_gpt4(prompt)


def handle_dictations(user_input):
    prompt = f"""
You are transcribing a judge's dictation into a formal court order or judgment in the Pakistani legal context.

Dictation: {user_input}
"""
    return call_gpt4(prompt)
