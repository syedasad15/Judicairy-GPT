# prompt_map.py
from Agents import (
    clerk,
    stenographer,
    typist,
    bench_assistant,
    judicial_assistant,
    bailiff,
    registrar,
    generic_agent,
    judgement_agent,
    websearch
)

PROMPT_MAP = {
    # Judicial Assistant
    "Research Laws": judicial_assistant.research_case_laws,
    "Draft Legal Briefs": judicial_assistant.draft_legal_briefs,
    "Track Legal Updates": judicial_assistant.track_updates,
    "Review Memo": judicial_assistant.prepare_memos,
    "Web Search": websearch.websearch_with_citations, 
    # Clerk
    "Summarize Files": clerk.prepare_case_files,
    "Notify Parties": clerk.notify_parties,
    "Update Cause List": clerk.manage_cause_list,
    "Update Registers": clerk.update_registers,
    "Present Briefs": clerk.present_case_briefs,

    # Stenographer
    "Draft Judgment": stenographer.type_judgments,
    "Format Orders": stenographer.format_orders,
    "Proofread Drafts": stenographer.proofread_drafts,
    "Handle Dictations": stenographer.handle_dictations,

    # Typist
    "Type Orders/Letters": typist.type_documents,
    "Format Order": typist.format_documents,
    "Distribute Documents": typist.print_and_distribute,

    # Bench Assistant
    "Prepare Courtroom": bench_assistant.prepare_courtroom,
    "Mark Evidence": bench_assistant.mark_evidence,
    "Call Cases": bench_assistant.call_cases,
    "Handle Case Files": bench_assistant.manage_files,

    # Bailiff
    "Deliver Summons": bailiff.serve_summons,
    "Maintain Court Order": bailiff.maintain_order,
    "Escort Judge/Witnesses": bailiff.escort_parties,
    "Call Parties": bailiff.call_parties,

    # Registrar
    "Admin Status": registrar.prepare_reports,
    "Manage Communication": registrar.manage_communication,
    "Supervise Staff": registrar.supervise_staff,
    "Manage Calendar": registrar.manage_calendar,

    # Generic
    "generic": generic_agent.generic_agent,
    "generate_legal_judgment": judgement_agent.generate_legal_judgment
}

