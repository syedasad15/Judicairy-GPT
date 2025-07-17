from utils.gpt_client import call_gpt4

def research_case_laws(user_input):
    prompt = f"""
You are a legal assistant to a Pakistani judge. Based on the query below, provide a summary of relevant Pakistani case laws, legal provisions, and precedents.

Query: {user_input}

Ensure your response:
- Is strictly based on Pakistani laws and jurisprudence
- Includes case references where applicable
- Is structured for courtroom utility
"""
    return call_gpt4(prompt)


def draft_legal_briefs(user_input):
    prompt = f"""
You are drafting a legal brief for a Pakistani judge.

Task: {user_input}

Make sure the brief is:
- Based only on Pakistani law
- Written in formal judicial language
- Includes references to applicable statutes and precedents
"""
    return call_gpt4(prompt)


def track_updates(user_input):
    prompt = f"""
You are tracking recent legislative and judicial updates in Pakistan related to:

{user_input}

Return a formal summary that includes:
- New amendments or case law
- Court rulings or clarifications
- How it affects existing legal interpretation
"""
    return call_gpt4(prompt)


def prepare_memos(user_input):
    prompt = f"""
Prepare a professional judicial memo summarizing the following topic or case-related issue:

{user_input}

Use formal structure and limit it to Pakistani jurisdiction only.
"""
    return call_gpt4(prompt)


def generate_case_decision(case_text):
    prompt = f"""
You are a senior judge in the Pakistani judicial system.
Below is a case summary or detailed case file.

Your task:
- Analyze the facts
- Apply relevant Pakistani laws
- Write a judgment/decision
- Include citations to actual laws (like PPC, CrPC, Evidence Act, etc.)

CASE FILE:
\"\"\"
{case_text}
\"\"\"

Return only the final judgment in a formal legal format.
    """
    return call_gpt4(prompt).strip()
