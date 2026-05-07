from __future__ import annotations

from typing import Any

from founder_sales_os.utils import (
    clamp_score,
    find_keywords,
    normalize_keyword_groups,
    normalize_text,
    role_is_decision_maker,
    text_blob,
)


def score_icp_fit(record: dict[str, Any], intelligence: dict[str, Any], company_profile: dict[str, Any], scoring_rules: dict[str, Any]) -> dict[str, Any]:
    weights = scoring_rules.get("icp_fit", {}).get("weights", {})
    employee_range = scoring_rules.get("icp_fit", {}).get("employee_count", {})
    score = 0
    reasons: list[str] = []
    risks: list[str] = []

    industry = normalize_text(record.get("industry"))
    target_industries = [normalize_text(item) for item in company_profile.get("target_industries", [])]
    if industry in target_industries:
        score += weights.get("target_industry", 0)
        reasons.append(f"Target industry: {record.get('industry')}")

    stage = normalize_text(record.get("company_stage"))
    target_stages = [normalize_text(item) for item in company_profile.get("target_company_stages", [])]
    if stage in target_stages:
        score += weights.get("target_stage", 0)
        reasons.append(f"Target company stage: {record.get('company_stage')}")

    employee_count = int(record.get("employee_count", 0))
    if employee_range.get("min", 0) <= employee_count <= employee_range.get("max", 10_000):
        score += weights.get("employee_count_fit", 0)
        reasons.append(f"Employee count in target range: {employee_count}")

    if role_is_decision_maker(record.get("contact_role")):
        score += weights.get("decision_maker_contact", 0)
        reasons.append(f"Decision-maker involved: {record.get('contact_role')}")
    else:
        risks.append("Decision-maker not confirmed")

    blob = text_blob(record)
    strong_signals = find_keywords(blob, company_profile.get("strong_fit_signals", []))
    if strong_signals:
        score += weights.get("strong_fit_signal", 0)
        reasons.append("Strong fit signal: " + strong_signals[0])

    weak_signals = find_keywords(blob, company_profile.get("weak_fit_signals", []))
    if weak_signals:
        score += weights.get("weak_fit_penalty", 0)
        risks.append("Weak fit signal: " + weak_signals[0])

    disqualifiers = find_keywords(blob, company_profile.get("disqualifiers", []))
    if disqualifiers:
        score += weights.get("disqualifier_penalty", 0)
        risks.append("Disqualifier: " + disqualifiers[0])

    if (
        normalize_text(record.get("stated_pain"))
        and intelligence.get("pain_category") != "general sales learning"
        and not weak_signals
        and not disqualifiers
    ):
        score += weights.get("pain_relevance", 0)
        reasons.append(f"Relevant pain: {intelligence.get('pain_category')}")

    final_score = clamp_score(score)
    return {
        "icp_fit_score": final_score,
        "fit_category": fit_category(final_score, scoring_rules),
        "top_fit_reasons": "; ".join((reasons + risks)[:5]) if reasons or risks else "No clear fit reasons detected",
    }


def fit_category(score: int, scoring_rules: dict[str, Any]) -> str:
    boundaries = scoring_rules.get("score_boundaries", {})
    if score >= boundaries.get("strong_fit_min", 75):
        return "Strong fit"
    if score >= boundaries.get("medium_fit_min", 50):
        return "Medium fit"
    return "Weak fit"


def score_deal_signals(record: dict[str, Any], intelligence: dict[str, Any], scoring_rules: dict[str, Any]) -> dict[str, int]:
    blob = text_blob(record)
    pain_score = score_keyword_band(blob, scoring_rules.get("pain_intensity", {}), default_when_present=55)
    urgency_score = score_urgency(intelligence.get("urgency_signals", ""))
    budget_score = score_budget(intelligence.get("budget_signals", ""))
    follow_up_score = score_follow_up(record, scoring_rules)
    pitch_clarity_score = score_pitch_clarity(intelligence, scoring_rules)
    implementation_risk_score = 80 if "Implementation risk" in intelligence.get("risk_flags", "") else 20
    competitor_risk_score = 75 if "Competitor comparison risk" in intelligence.get("risk_flags", "") else 10

    rescue_score = score_rescue_priority(
        icp_fit_score=int(intelligence.get("icp_fit_score", 0)),
        pain_intensity_score=pain_score,
        urgency_score=urgency_score,
        budget_score=budget_score,
        follow_up_clarity_score=follow_up_score,
        pitch_clarity_score=pitch_clarity_score,
        implementation_risk_score=implementation_risk_score,
        competitor_risk_score=competitor_risk_score,
        intelligence=intelligence,
        scoring_rules=scoring_rules,
    )

    return {
        "pain_intensity_score": pain_score,
        "urgency_score": urgency_score,
        "budget_score": budget_score,
        "follow_up_clarity_score": follow_up_score,
        "pitch_clarity_score": pitch_clarity_score,
        "implementation_risk_score": implementation_risk_score,
        "competitor_risk_score": competitor_risk_score,
        "deal_rescue_priority_score": rescue_score,
    }


def score_keyword_band(blob: str, rules: dict[str, Any], default_when_present: int = 0) -> int:
    text = normalize_text(blob)
    if find_keywords(text, rules.get("high_keywords", [])):
        return 90
    if find_keywords(text, rules.get("medium_keywords", [])):
        return 60
    if find_keywords(text, rules.get("low_keywords", [])):
        return 20
    return default_when_present if text else 0


def score_urgency(urgency_signals: Any) -> int:
    text = normalize_text(urgency_signals)
    if "high urgency" in text:
        return 90
    if "medium urgency" in text:
        return 60
    if "low urgency" in text:
        return 20
    return 35 if text and text != "none detected" else 0


def score_budget(budget_signals: Any) -> int:
    text = normalize_text(budget_signals)
    if text == "no budget signal detected":
        return 0
    if "high budget" in text:
        return 85
    if "medium budget" in text or "mentioned but not clear" in text:
        return 55
    if "low budget" in text or "no budget" in text:
        return 15
    return 0


def score_follow_up(record: dict[str, Any], scoring_rules: dict[str, Any]) -> int:
    next_step = normalize_text(record.get("next_step"))
    rules = scoring_rules.get("follow_up_clarity", {})
    clear = find_keywords(next_step, rules.get("clear_next_step_keywords", []))
    vague = find_keywords(next_step, rules.get("vague_next_step_keywords", []))
    if clear:
        return 90
    if vague or not next_step:
        return 25
    return 55


def score_pitch_clarity(intelligence: dict[str, Any], scoring_rules: dict[str, Any]) -> int:
    rules = scoring_rules.get("pitch_clarity", {})
    confusion_count = 0 if intelligence.get("pitch_confusion_signals") == "None detected" else len(str(intelligence.get("pitch_confusion_signals", "")).split(";"))
    narrative_count = 0 if intelligence.get("narrative_gaps") == "None detected" else len(str(intelligence.get("narrative_gaps", "")).split(";"))
    score = 100
    score -= confusion_count * rules.get("confusion_penalty_per_signal", 15)
    score -= narrative_count * rules.get("narrative_gap_penalty_per_signal", 10)
    return clamp_score(score)


def score_rescue_priority(
    icp_fit_score: int,
    pain_intensity_score: int,
    urgency_score: int,
    budget_score: int,
    follow_up_clarity_score: int,
    pitch_clarity_score: int,
    implementation_risk_score: int,
    competitor_risk_score: int,
    intelligence: dict[str, Any],
    scoring_rules: dict[str, Any],
) -> int:
    weights = scoring_rules.get("deal_rescue_priority", {}).get("weights", {})
    score = (
        icp_fit_score * weights.get("icp_fit_score", 0.25)
        + pain_intensity_score * weights.get("pain_intensity_score", 0.20)
        + urgency_score * weights.get("urgency_score", 0.15)
        + budget_score * weights.get("budget_score", 0.10)
    )

    risk_flags = normalize_text(intelligence.get("risk_flags"))
    if intelligence.get("extracted_objections") != "None detected":
        score += weights.get("unresolved_objection_risk", 15)
    if follow_up_clarity_score < 60 or "next step needs tightening" in risk_flags:
        score += weights.get("unclear_next_step_risk", 15)
    if competitor_risk_score >= 70:
        score += weights.get("competitor_risk", 8)
    if pitch_clarity_score < 80:
        score += weights.get("pitch_confusion_risk", 8)
    if implementation_risk_score >= 70:
        score += weights.get("implementation_risk_penalty", 6)

    return clamp_score(score)


def detect_strong_fit_signal(record: dict[str, Any], company_profile: dict[str, Any]) -> bool:
    groups = normalize_keyword_groups({"strong": company_profile.get("strong_fit_signals", [])})
    return bool(find_keywords(text_blob(record), groups["strong"]))
