from utils.gpt_client import call_gpt4

def prepare_case_files(user_input):
    prompt = f"""
Summarize the following case file for judicial review in Pakistan. Focus on:
- Key facts
- Legal questions
- Applicable Pakistani laws

Content: {user_input}
"""
    return call_gpt4(prompt)


def notify_parties(user_input):
    prompt = f"""
Draft a notification message to relevant parties regarding the following matter:

{user_input}

Format it for official use in a Pakistani court.
"""
    return call_gpt4(prompt)


def manage_cause_list(user_input):
    prompt = f"""
Update the cause list based on the following court activities or changes:

{user_input}

Use standard formatting and include court room, case numbers, and parties.
"""
    return call_gpt4(prompt)


def update_registers(user_input):
    prompt = f"""
You are updating judicial registers. Describe what register entries should be made based on this input:

{user_input}

Follow proper format used in Pakistani lower and high courts.
"""
    return call_gpt4(prompt)


def present_case_briefs(user_input):
    prompt = f"""
Prepare a short case brief for a Pakistani judge.

Input: {user_input}

Include: facts, legal issue, and decision summary. Keep it concise.
"""
    return call_gpt4(prompt)
