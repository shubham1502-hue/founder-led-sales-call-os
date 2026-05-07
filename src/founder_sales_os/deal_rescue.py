from __future__ import annotations

import pandas as pd


ACTIVE_STAGE_EXCLUSIONS = {"closed won", "closed lost", "lost", "won"}


def build_deal_rescue_queue(call_intelligence: pd.DataFrame, scoring_rules: dict) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    active = call_intelligence[
        ~call_intelligence["deal_stage"].str.lower().isin(ACTIVE_STAGE_EXCLUSIONS)
    ].copy()
    active = active.sort_values(
        by=["deal_rescue_priority_score", "icp_fit_score", "pain_intensity_score"],
        ascending=False,
    )

    for index, row in enumerate(active.to_dict("records"), start=1):
        priority = classify_rescue_priority(row, scoring_rules)
        if row.get("fit_category") == "Weak fit" and priority != "High":
            continue
        if priority == "Low" and row.get("fit_category") == "Weak fit" and int(row.get("urgency_score", 0)) < 40:
            continue

        reason = build_reason(row)
        rows.append(
            {
                "task_id": f"DRQ-{index:03d}",
                "company_name": row["company_name"],
                "priority": priority,
                "deal_stage": row["deal_stage"],
                "founder_next_action": row["founder_next_action"],
                "reason": reason,
                "suggested_followup_message": suggested_followup_message(row),
                "due_timing": due_timing(priority, row),
                "rescue_risk": rescue_risk(row),
                "expected_leverage": expected_leverage(row),
                "_priority_rank": {"High": 0, "Medium": 1, "Low": 2}.get(priority, 3),
                "_score": row.get("deal_rescue_priority_score", 0),
            }
        )

    queue = pd.DataFrame(
        rows,
        columns=[
            "task_id",
            "company_name",
            "priority",
            "deal_stage",
            "founder_next_action",
            "reason",
            "suggested_followup_message",
            "due_timing",
            "rescue_risk",
            "expected_leverage",
            "_priority_rank",
            "_score",
        ],
    )
    if not queue.empty:
        queue = queue.sort_values(["_priority_rank", "_score", "company_name"], ascending=[True, False, True]).reset_index(drop=True)
        queue["task_id"] = [f"DRQ-{index:03d}" for index in range(1, len(queue) + 1)]
    return queue.drop(columns=["_priority_rank", "_score"], errors="ignore")


def classify_rescue_priority(row: dict, scoring_rules: dict) -> str:
    score = int(row.get("deal_rescue_priority_score", 0))
    priority_rules = scoring_rules.get("deal_rescue_priority", {})
    high_min = priority_rules.get("high_min_score", 70)
    medium_min = priority_rules.get("medium_min_score", 45)
    risk_flags = str(row.get("risk_flags", ""))

    if str(row.get("deal_stage", "")).lower() == "discovery" and "Weak urgency" in risk_flags and "Budget risk" in risk_flags:
        return "Low"

    if row.get("fit_category") == "Strong fit" and int(row.get("pain_intensity_score", 0)) >= 80 and int(row.get("follow_up_clarity_score", 0)) < 60:
        return "High"
    if (
        str(row.get("deal_stage", "")).lower() in {"proposal", "pilot", "negotiation"}
        and int(row.get("urgency_score", 0)) >= 80
        and int(row.get("budget_score", 0)) >= 55
        and row.get("extracted_objections") != "None detected"
    ):
        return "High"
    if score >= high_min:
        return "High"
    if score >= medium_min:
        return "Medium"
    return "Low"


def build_reason(row: dict) -> str:
    parts: list[str] = []
    parts.append(f"{row.get('fit_category')} with ICP score {row.get('icp_fit_score')}")
    if int(row.get("pain_intensity_score", 0)) >= 80:
        parts.append("strong pain")
    if int(row.get("urgency_score", 0)) >= 80:
        parts.append("time-sensitive urgency")
    if int(row.get("budget_score", 0)) >= 55:
        parts.append("budget signal present")
    if "Next step needs tightening" in str(row.get("risk_flags")):
        parts.append("next step is not tight enough")
    if row.get("extracted_objections") != "None detected":
        parts.append(f"objection unresolved: {row.get('extracted_objections')}")
    return "; ".join(parts)


def suggested_followup_message(row: dict) -> str:
    company = row.get("company_name", "your team")
    action = row.get("founder_next_action", "send a clear recap")
    objection = row.get("extracted_objections", "the main blocker")
    return (
        f"Thanks for the call. I pulled out the main blocker as {objection}. "
        f"My suggested next step is: {action} "
        f"Would it be useful to pressure-test this with the right owner this week?"
    )


def due_timing(priority: str, row: dict) -> str:
    if priority == "High":
        return "Within 24 hours"
    if int(row.get("urgency_score", 0)) >= 80:
        return "This week"
    if priority == "Medium":
        return "Within 2 business days"
    return "Review during weekly GTM meeting"


def rescue_risk(row: dict) -> str:
    flags = str(row.get("risk_flags", ""))
    if "Pitch confusion" in flags:
        return "Prospect may misunderstand the category and compare against the wrong tool."
    if "Competitor comparison risk" in flags:
        return "Prospect may default to an existing CRM or call recording tool."
    if "Next step needs tightening" in flags:
        return "Momentum may stall because the next step is not concrete."
    if "Budget risk" in flags:
        return "Pain may be real but unfunded."
    return "Deal may drift without founder-owned follow-up."


def expected_leverage(row: dict) -> str:
    if row.get("fit_category") == "Strong fit" and int(row.get("pain_intensity_score", 0)) >= 80:
        return "High leverage because a founder response can convert live pain into a clear next step."
    if int(row.get("budget_score", 0)) >= 55:
        return "Medium leverage because budget exists but the blocker still needs a sharper proof point."
    if row.get("fit_category") == "Weak fit":
        return "Low leverage. Use the learning, but avoid over-investing founder time."
    return "Medium leverage if the founder clarifies ownership, proof, and timing."
