from utils.gpt_client import call_gpt4
from prompt_map import PROMPT_MAP

def classify_prompt_intent(user_input):
    system_commands = list(PROMPT_MAP.keys())
    formatted_commands = "\n".join(f"- {cmd}" for cmd in system_commands)

    prompt = f"""
You are an intent classification assistant for a legal chatbot used in the judicial system of Pakistan.

Your job is to classify the user's request by matching it to one of the exact system command labels below, even if the user makes minor spelling mistakes, grammatical issues, or uses synonyms.

Here are the available commands:
{formatted_commands}

User's Input:
"{user_input}"

Instructions:
- Respond ONLY with the closest matching command (case-sensitive).
- If no match is found after considering small typos or synonyms, respond with "Unknown".
- Do not explain your answer or add anything else.

Output:
"""

    result = call_gpt4(prompt).strip()
    return result
