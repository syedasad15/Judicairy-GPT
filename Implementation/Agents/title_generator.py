from utils.gpt_client import call_gpt4

def generate_chat_title(user_prompt: str) -> str:
    """
    Generates a concise, relevant title for a chat based on the user's prompt.
    """

    prompt = f"""
You are a legal assistant helping organize conversations in a legal chatbot system.

Given the following user input, generate a very short and descriptive title (3–7 words) that reflects the topic or intent of the prompt.

- Avoid using generic titles like "New Chat".
- Capitalize each word.
- Do NOT include quotation marks or punctuation.
- Be specific to the legal domain if possible.

User Prompt:
\"{user_prompt}\"

Title:
"""

    response = call_gpt4(prompt).strip()
    return response
