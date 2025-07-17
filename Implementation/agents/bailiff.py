from utils.gpt_client import call_gpt4

def serve_summons(user_input):
    prompt = f"""
Draft an official format for delivering a summons to the party described below:

{user_input}
"""
    return call_gpt4(prompt)


def maintain_order(user_input):
    prompt = f"""
Summarize procedures for maintaining court discipline based on this situation:

{user_input}
"""
    return call_gpt4(prompt)


def escort_parties(user_input):
    prompt = f"""
Based on this instruction, prepare directions for escorting judges or witnesses securely:

{user_input}
"""
    return call_gpt4(prompt)


def call_parties(user_input):
    prompt = f"""
Announce the presence of the following parties in the courtroom:

{user_input}
"""
    return call_gpt4(prompt)
