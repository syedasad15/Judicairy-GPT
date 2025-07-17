from utils.gpt_client import call_gpt4

def type_documents(user_input):
    prompt = f"""
Type the following order or letter using official court language and formatting used in Pakistan:

{user_input}
"""
    return call_gpt4(prompt)


def format_documents(user_input):
    prompt = f"""
Format the following legal text as per judicial norms in Pakistan:

{user_input}
"""
    return call_gpt4(prompt)


def print_and_distribute(user_input):
    prompt = f"""
Prepare a final version of this court document for printing and distribution to involved parties:

{user_input}

Make sure the language is final and no further edits are needed.
"""
    return call_gpt4(prompt)
