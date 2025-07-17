from utils.gpt_client import call_gpt4

def prepare_reports(user_input):
    prompt = f"""
Prepare an administrative status report for the court registry on the following matter:

{user_input}

Use bullet points or sections as appropriate.
"""
    return call_gpt4(prompt)


def manage_communication(user_input):
    prompt = f"""
Draft an official communication or letter to stakeholders based on:

{user_input}

Ensure it reflects judicial office protocol.
"""
    return call_gpt4(prompt)


def supervise_staff(user_input):
    prompt = f"""
Summarize staff supervision or disciplinary actions based on:

{user_input}
"""
    return call_gpt4(prompt)


def manage_calendar(user_input):
    prompt = f"""
Update or manage the court calendar based on:

{user_input}

Format it clearly for use in judge’s chamber.
"""
    return call_gpt4(prompt)
