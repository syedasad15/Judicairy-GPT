from utils.gpt_client import call_gpt4

def generic_agent(prompt: str) -> str:
    """
    Responds to legal queries that don't match a specific predefined intent.
    Acts as a general-purpose assistant for Pakistan's judicial system.
    """
    system_prompt = (
        "You are a knowledgeable and helpful legal assistant trained in the Pakistani judicial system. "
        "You will be provided with user queries and/or case details. "
        "Respond clearly, accurately, and with relevant legal insight."
    )

    final_prompt = f"{system_prompt}\n\nUser Query:\n{prompt}"
    return call_gpt4(final_prompt)
