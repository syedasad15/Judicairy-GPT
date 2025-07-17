from utils.gpt_client import call_gpt4
def generate_legal_judgment(prompt):
    system_prompt = (
        "You are a senior Pakistani judge. Based on the following case file and details, "
        "generate a formal legal judgment in proper format:\n\n"
    )
    return call_gpt4(system_prompt + prompt)