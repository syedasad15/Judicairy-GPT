from utils.intent_classifier import classify_prompt_intent
from prompt_map import PROMPT_MAP
from utils.gpt_client import call_gpt4
from prompt_router import classify_prompt_intent, PROMPT_MAP
from streamlit import session_state as st_session
from utils.gpt_client import call_gpt4
from prompt_router import classify_prompt_intent, PROMPT_MAP
from streamlit import session_state as st_session

from prompt_router import classify_prompt_intent, PROMPT_MAP
from streamlit import session_state as st_session

def handle_user_input(user_input):
    # Combine uploaded case text if present
    case_text = st_session.get("uploaded_case_text", "")
    if case_text:
        user_input = f"The following case has been uploaded:\n\n{case_text}\n\nNow respond to the user's request:\n{user_input}"

    matched_command = classify_prompt_intent(user_input)

    # Use matched command or fall back to "generic"
    handler_function = PROMPT_MAP.get(matched_command, PROMPT_MAP["generic"])
    print(f"[INFO] Routing input to: {matched_command if matched_command in PROMPT_MAP else 'generic'}")

    return handler_function(user_input)



def generate_title_from_prompt(prompt: str) -> str:
    """
    Generates a short, concise title for the given legal prompt.
    Designed to be used as a chat session name.
    """
    title_prompt = (
        f"Summarize the following legal prompt into a concise 3 to 6 word title:\n\n"
        f"{prompt}\n\n"
        f"Only return the title, without extra explanation."
    )
    
    # Replace this with your actual LLM handler
    response = call_gpt4(title_prompt)  # or whatever function you're using
    return response.strip().strip('"')