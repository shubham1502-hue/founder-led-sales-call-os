from __future__ import annotations

from typing import Any

from founder_sales_os.utils import (
    coerce_text,
    find_group_matches,
    find_keywords,
    humanize_label,
    join_values,
    labels_from_matches,
    normalize_keyword_groups,
    normalize_text,
    role_is_decision_maker,
    text_blob,
)


OBJECTION_RESPONSE_LIBRARY: dict[str, dict[str, str]] = {
    "price": {
        "suggested_response_angle": "Tie cost to recovered founder time, fewer slipped follow-ups, and rescued late-stage deals.",
        "product_or_narrative_implication": "Lead with revenue leakage and time saved, not software features.",
        "recommended_proof_point": "Show a before and after weekly memo plus one rescued deal example.",
    },
    "timing": {
        "suggested_response_angle": "Connect the system to the next board, pipeline, or founder review date.",
        "product_or_narrative_implication": "Make the weekly operating rhythm feel immediate.",
        "recommended_proof_point": "Use a 7-day sales learning loop example.",
    },
    "switching_cost": {
        "suggested_response_angle": "Position the workflow as an export and synthesis layer, not a CRM replacement.",
        "product_or_narrative_implication": "Emphasize low migration and compatibility with current notes.",
        "recommended_proof_point": "Show a CSV import from existing CRM notes.",
    },
    "internal_bandwidth": {
        "suggested_response_angle": "Offer a lightweight Friday export and memo workflow that avoids new process overhead.",
        "product_or_narrative_implication": "Make setup feel founder-led and fast.",
        "recommended_proof_point": "Show the exact 10-minute workflow.",
    },
    "security": {
        "suggested_response_angle": "Explain offline operation, anonymized examples, and data-minimizing usage.",
        "product_or_narrative_implication": "Security and privacy need to appear before feature depth.",
        "recommended_proof_point": "Provide an anonymized sample output and security checklist.",
    },
    "integrations": {
        "suggested_response_angle": "Start with CSV exports from the tools they already use before promising automation.",
        "product_or_narrative_implication": "Frame integrations as workflow convenience, not core value.",
        "recommended_proof_point": "Show HubSpot, Salesforce, Attio, or Pipedrive CSV import examples.",
    },
    "unclear_roi": {
        "suggested_response_angle": "Quantify slipped follow-ups, repeated objections, and founder intervention leverage.",
        "product_or_narrative_implication": "Use ROI language around rescued pipeline and faster narrative iteration.",
        "recommended_proof_point": "Show objection trend counts and deal rescue queue examples.",
    },
    "lack_of_urgency": {
        "suggested_response_angle": "Ask what will happen if the same objections repeat for another month.",
        "product_or_narrative_implication": "Add sharper why-now language.",
        "recommended_proof_point": "Show a weekly learning loop that compounds over five calls.",
    },
    "stakeholder_alignment": {
        "suggested_response_angle": "Create stakeholder-specific recap notes and founder-to-founder follow-up paths.",
        "product_or_narrative_implication": "Show how the OS exposes blocker ownership.",
        "recommended_proof_point": "Use a champion versus economic buyer risk example.",
    },
    "competitor_comparison": {
        "suggested_response_angle": "Contrast call recording and CRM storage with founder learning and deal rescue.",
        "product_or_narrative_implication": "Sharpen category framing against recording tools and CRMs.",
        "recommended_proof_point": "Show output files that Gong or CRM notes do not create by default.",
    },
}


PAIN_CATEGORIES: dict[str, list[str]] = {
    "follow-up leakage": ["follow-up", "follow up", "slipping", "forgot", "memory"],
    "objection pattern visibility": ["objection", "repeat", "pattern", "asks about"],
    "pipeline risk visibility": ["deal risk", "stalled", "pipeline", "forecast", "blocked"],
    "narrative clarity": ["pitch", "positioning", "homepage", "deck", "messaging", "category"],
    "implementation confidence": ["implementation", "integration", "migration", "security", "privacy"],
    "weekly gtm learning": ["weekly", "memo", "review", "board", "learning"],
}


def extract_call_intelligence(
    record: dict[str, Any],
    company_profile: dict[str, Any],
    scoring_rules: dict[str, Any] | None = None,
) -> dict[str, Any]:
    blob = text_blob(record)

    objection_groups = normalize_keyword_groups(company_profile.get("objection_keywords", {}))
    objection_matches = find_group_matches(blob, objection_groups)
    objection_labels = labels_from_matches(objection_matches)

    competitor_mentions = extract_competitor_mentions(blob, company_profile)
    buying_triggers = find_keywords(blob, company_profile.get("buying_trigger_keywords", []))
    urgency_signals = extract_urgency_signals(blob, company_profile)
    budget_signals = extract_budget_signals(blob, scoring_rules or {})
    confusion_signals = find_keywords(blob, company_profile.get("confusion_keywords", []))
    narrative_gaps = find_keywords(blob, company_profile.get("narrative_gap_keywords", []))
    pain_category = classify_pain(blob)
    risk_flags = build_risk_flags(
        record=record,
        objections=objection_labels,
        competitor_mentions=competitor_mentions,
        confusion_signals=confusion_signals,
        urgency_signals=urgency_signals,
        budget_signals=budget_signals,
        scoring_rules=scoring_rules or {},
    )
    founder_next_action = recommend_founder_next_action(
        record=record,
        objections=objection_labels,
        risk_flags=risk_flags,
        competitor_mentions=competitor_mentions,
        urgency_signals=urgency_signals,
        confusion_signals=confusion_signals,
    )

    return {
        "extracted_objections": join_values(humanize_label(label) for label in objection_labels),
        "buying_triggers": join_values(buying_triggers),
        "competitor_mentions": join_values(competitor_mentions),
        "urgency_signals": join_values(urgency_signals),
        "budget_signals": budget_signals,
        "pain_category": pain_category,
        "pitch_confusion_signals": join_values(confusion_signals),
        "narrative_gaps": join_values(narrative_gaps),
        "risk_flags": join_values(risk_flags),
        "founder_next_action": founder_next_action,
        "decision_maker_signal": "Decision-maker involved" if role_is_decision_maker(record.get("contact_role")) else "Decision-maker not confirmed",
    }


def extract_competitor_mentions(blob: str, company_profile: dict[str, Any]) -> list[str]:
    keywords = company_profile.get("competitor_keywords", [])
    found = find_keywords(blob, keywords)
    return [keyword.title() if keyword.islower() else keyword for keyword in found]


def extract_urgency_signals(blob: str, company_profile: dict[str, Any]) -> list[str]:
    groups = normalize_keyword_groups(company_profile.get("urgency_keywords", {}))
    matches = find_group_matches(blob, groups)
    signals: list[str] = []
    for level in ("high", "medium", "low", "signals"):
        for keyword in matches.get(level, []):
            signals.append(f"{humanize_label(level)} urgency: {keyword}" if level != "signals" else keyword)
    return signals


def extract_budget_signals(blob: str, scoring_rules: dict[str, Any]) -> str:
    budget_rules = scoring_rules.get("budget_signal", {})
    high = find_keywords(blob, budget_rules.get("high_keywords", []))
    medium = find_keywords(blob, budget_rules.get("medium_keywords", []))
    low = find_keywords(blob, budget_rules.get("low_keywords", []))
    if high:
        return "High budget signal: " + ", ".join(high)
    if medium:
        return "Medium budget signal: " + ", ".join(medium)
    if low:
        return "Low budget signal: " + ", ".join(low)
    if "budget" in normalize_text(blob):
        return "Budget mentioned but not clear"
    return "No budget signal detected"


def classify_pain(blob: str) -> str:
    text = normalize_text(blob)
    best_label = "general sales learning"
    best_count = 0
    for label, keywords in PAIN_CATEGORIES.items():
        count = sum(1 for keyword in keywords if keyword in text)
        if count > best_count:
            best_count = count
            best_label = label
    return best_label


def build_risk_flags(
    record: dict[str, Any],
    objections: list[str],
    competitor_mentions: list[str],
    confusion_signals: list[str],
    urgency_signals: list[str],
    budget_signals: str,
    scoring_rules: dict[str, Any],
) -> list[str]:
    flags: list[str] = []
    next_step = normalize_text(record.get("next_step"))
    timeline = normalize_text(record.get("timeline_signal"))
    blob = text_blob(record)

    if objections:
        flags.append("Unresolved objection")
    if has_competitor_comparison_risk(record, objections):
        flags.append("Competitor comparison risk")
    if confusion_signals:
        flags.append("Pitch confusion")
    normalized_budget = normalize_text(budget_signals)
    if "low budget" in normalized_budget or normalized_budget == "no budget":
        flags.append("Budget risk")
    if any(term in timeline for term in ("no rush", "later", "next quarter", "maybe")):
        flags.append("Weak urgency")

    clear_keywords = scoring_rules.get("follow_up_clarity", {}).get("clear_next_step_keywords", [])
    vague_keywords = scoring_rules.get("follow_up_clarity", {}).get("vague_next_step_keywords", [])
    if not next_step or find_keywords(next_step, vague_keywords) or not find_keywords(next_step, clear_keywords):
        flags.append("Next step needs tightening")

    implementation_keywords = scoring_rules.get("implementation_risk", {}).get("keywords", [])
    if find_keywords(blob, implementation_keywords):
        flags.append("Implementation risk")
    if not role_is_decision_maker(record.get("contact_role")):
        flags.append("Founder or decision-maker not confirmed")
    if urgency_signals and any(signal.startswith("High urgency") for signal in urgency_signals):
        flags.append("Time-sensitive follow-up")
    return flags


def recommend_founder_next_action(
    record: dict[str, Any],
    objections: list[str],
    risk_flags: list[str],
    competitor_mentions: list[str],
    urgency_signals: list[str],
    confusion_signals: list[str],
) -> str:
    company = coerce_text(record.get("company_name")) or "the prospect"
    has_high_urgency = any(signal.startswith("High urgency") for signal in urgency_signals)

    if "security" in objections:
        return f"Send {company} an offline-data and security proof pack, then ask for the exact review owner."
    if "integrations" in objections:
        return f"Map the current-tool export path for {company} and propose a low-migration pilot."
    if "stakeholder_alignment" in objections:
        return f"Ask for the missing stakeholder call and prepare a founder-led recap by buyer role."
    if "price" in objections or "unclear_roi" in objections:
        return f"Send a concise ROI angle tied to slipped follow-ups, rescued deals, and founder time."
    if confusion_signals:
        return f"Send a sharper category explanation and one before-after example before asking for the next call."
    if "competitor_comparison" in objections:
        return f"Send a competitor comparison focused on post-call learning, not call recording or CRM storage."
    if "Next step needs tightening" in risk_flags:
        return f"Send a direct recap with one decision question and a dated next-step request."
    if has_high_urgency:
        return f"Book a founder rescue session this week and focus only on the active blocker."
    return f"Send a call recap with the objection, trigger, owner, and next step in one message."


def has_competitor_comparison_risk(record: dict[str, Any], objections: list[str]) -> bool:
    if "competitor_comparison" in objections:
        return True
    notes = normalize_text(record.get("call_notes"))
    comparison_phrases = (
        "different from",
        "compare with",
        "competitor comparison",
        "already has",
        "already using",
        "using gong",
        "using fireflies",
        "gong already",
        "hubspot has",
        "salesforce has",
        "attio has",
    )
    return any(phrase in notes for phrase in comparison_phrases)
