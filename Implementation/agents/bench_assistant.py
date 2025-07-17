from utils.gpt_client import call_gpt4

def prepare_courtroom(user_input):
    prompt = f"""
Based on the following instructions, outline the tasks to prepare the courtroom accordingly:

{user_input}
"""
    return call_gpt4(prompt)


def mark_evidence(user_input):
    prompt = f"""
Explain how to mark and record the following evidence for judicial proceedings in Pakistan:

{user_input}
"""
    return call_gpt4(prompt)


def call_cases(user_input):
    prompt = f"""
Announce and record the calling of the following cases in the cause list:

{user_input}
"""
    return call_gpt4(prompt)


def manage_files(user_input):
    prompt = f"""
Based on this case-related input, describe how the bench assistant should handle or organize the files:

{user_input}
"""
    return call_gpt4(prompt)
