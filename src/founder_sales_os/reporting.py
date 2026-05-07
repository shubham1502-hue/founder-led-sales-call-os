from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from founder_sales_os.deal_rescue import build_deal_rescue_queue
from founder_sales_os.extraction import OBJECTION_RESPONSE_LIBRARY, extract_call_intelligence
from founder_sales_os.narrative import generate_narrative_experiments
from founder_sales_os.scoring import score_deal_signals, score_icp_fit
from founder_sales_os.utils import humanize_label, split_joined


CALL_INTELLIGENCE_COLUMNS = [
    "call_id",
    "company_name",
    "contact_role",
    "industry",
    "deal_stage",
    "extracted_objections",
    "buying_triggers",
    "competitor_mentions",
    "urgency_signals",
    "budget_signals",
    "pain_category",
    "pitch_confusion_signals",
    "narrative_gaps",
    "risk_flags",
    "founder_next_action",
    "icp_fit_score",
    "fit_category",
    "top_fit_reasons",
    "pain_intensity_score",
    "urgency_score",
    "budget_score",
    "follow_up_clarity_score",
    "pitch_clarity_score",
    "implementation_risk_score",
    "competitor_risk_score",
    "deal_rescue_priority_score",
]


def run_pipeline(
    sales_calls: pd.DataFrame,
    company_profile: dict[str, Any],
    scoring_rules: dict[str, Any],
    output_dir: str | Path,
) -> dict[str, Path]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    call_intelligence = build_call_intelligence(sales_calls, company_profile, scoring_rules)
    objection_bank = build_objection_bank(call_intelligence)
    deal_rescue_queue = build_deal_rescue_queue(call_intelligence, scoring_rules)

    paths = {
        "call_intelligence": output_path / "call_intelligence.csv",
        "objection_bank": output_path / "objection_bank.csv",
        "deal_rescue_queue": output_path / "deal_rescue_queue.csv",
        "weekly_sales_learning_memo": output_path / "weekly_sales_learning_memo.md",
        "narrative_experiments": output_path / "narrative_experiments.md",
    }
    call_intelligence.to_csv(paths["call_intelligence"], index=False)
    objection_bank.to_csv(paths["objection_bank"], index=False)
    deal_rescue_queue.to_csv(paths["deal_rescue_queue"], index=False)
    generate_weekly_memo(call_intelligence, objection_bank, deal_rescue_queue, paths["weekly_sales_learning_memo"])
    generate_narrative_experiments(call_intelligence, objection_bank, paths["narrative_experiments"])
    return paths


def build_call_intelligence(
    sales_calls: pd.DataFrame,
    company_profile: dict[str, Any],
    scoring_rules: dict[str, Any],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for record in sales_calls.to_dict("records"):
        extracted = extract_call_intelligence(record, company_profile, scoring_rules)
        icp = score_icp_fit(record, extracted, company_profile, scoring_rules)
        combined = {**record, **extracted, **icp}
        deal_scores = score_deal_signals(record, combined, scoring_rules)
        combined.update(deal_scores)
        rows.append({column: combined.get(column, "") for column in CALL_INTELLIGENCE_COLUMNS})
    return pd.DataFrame(rows, columns=CALL_INTELLIGENCE_COLUMNS)


def build_objection_bank(call_intelligence: pd.DataFrame) -> pd.DataFrame:
    objection_rows: list[dict[str, str]] = []
    for _, row in call_intelligence.iterrows():
        for objection in split_joined(row["extracted_objections"]):
            key = objection.lower().replace(" ", "_")
            library = OBJECTION_RESPONSE_LIBRARY.get(key, fallback_objection_library(objection))
            objection_rows.append(
                {
                    "objection_theme": objection,
                    "company_name": row["company_name"],
                    "suggested_response_angle": library["suggested_response_angle"],
                    "product_or_narrative_implication": library["product_or_narrative_implication"],
                    "recommended_proof_point": library["recommended_proof_point"],
                }
            )

    if not objection_rows:
        return pd.DataFrame(
            columns=[
                "objection_theme",
                "count",
                "example_companies",
                "suggested_response_angle",
                "product_or_narrative_implication",
                "recommended_proof_point",
            ]
        )

    raw = pd.DataFrame(objection_rows)
    grouped = (
        raw.groupby("objection_theme", as_index=False)
        .agg(
            count=("company_name", "count"),
            example_companies=("company_name", lambda values: "; ".join(list(values)[:3])),
            suggested_response_angle=("suggested_response_angle", "first"),
            product_or_narrative_implication=("product_or_narrative_implication", "first"),
            recommended_proof_point=("recommended_proof_point", "first"),
        )
        .sort_values(["count", "objection_theme"], ascending=[False, True])
    )
    return grouped


def fallback_objection_library(objection: str) -> dict[str, str]:
    label = humanize_label(objection)
    return {
        "suggested_response_angle": f"Clarify the business impact behind the {label.lower()} concern.",
        "product_or_narrative_implication": f"Add clearer messaging for {label.lower()} blockers.",
        "recommended_proof_point": f"Show a concrete example that addresses {label.lower()}.",
    }


def generate_weekly_memo(
    call_intelligence: pd.DataFrame,
    objection_bank: pd.DataFrame,
    deal_rescue_queue: pd.DataFrame,
    output_path: str | Path,
) -> str:
    memo = build_weekly_memo(call_intelligence, objection_bank, deal_rescue_queue)
    Path(output_path).write_text(memo, encoding="utf-8")
    return memo


def build_weekly_memo(
    call_intelligence: pd.DataFrame,
    objection_bank: pd.DataFrame,
    deal_rescue_queue: pd.DataFrame,
) -> str:
    total_calls = len(call_intelligence)
    strong_fit = int((call_intelligence["fit_category"] == "Strong fit").sum())
    medium_fit = int((call_intelligence["fit_category"] == "Medium fit").sum())
    weak_fit = int((call_intelligence["fit_category"] == "Weak fit").sum())
    high_rescue = int((deal_rescue_queue["priority"] == "High").sum()) if not deal_rescue_queue.empty else 0
    confused = call_intelligence[call_intelligence["pitch_confusion_signals"] != "None detected"]

    lines: list[str] = [
        "# Weekly Sales Learning Memo",
        "",
        "## Executive summary",
        f"- Reviewed {total_calls} founder-led sales calls.",
        f"- Pipeline quality: {strong_fit} strong-fit, {medium_fit} medium-fit, and {weak_fit} weak-fit opportunities.",
        f"- {high_rescue} deals need high-priority founder attention this week.",
        f"- The main learning loop is objections, pitch confusion, deal rescue, and next week's narrative tests.",
        "",
        "## What we learned from sales calls this week",
        "- Prospects respond best when the workflow is framed as post-call founder learning instead of another CRM or recording tool.",
        "- High-urgency teams already have scattered notes across CRM, Slack, Notion, and call recorders.",
        "- The strongest calls had a named operating moment such as a board meeting, pipeline review, procurement meeting, or stalled pilot.",
        "- Weak-fit calls tended to ask for outbound research or generic templates instead of post-call intelligence.",
        "",
        "## Pipeline quality snapshot",
        f"- Strong fit: {strong_fit}",
        f"- Medium fit: {medium_fit}",
        f"- Weak fit: {weak_fit}",
        f"- Average ICP fit score: {round(call_intelligence['icp_fit_score'].mean(), 1)}",
        f"- Average deal rescue priority score: {round(call_intelligence['deal_rescue_priority_score'].mean(), 1)}",
        "",
        "## Strongest ICP signals",
    ]
    strongest = call_intelligence.sort_values("icp_fit_score", ascending=False).head(5)
    for row in strongest.to_dict("records"):
        lines.append(f"- {row['company_name']}: {row['icp_fit_score']} ({row['top_fit_reasons']})")

    lines.extend(["", "## Most common objections"])
    if objection_bank.empty:
        lines.append("- No objections detected.")
    else:
        for row in objection_bank.head(7).to_dict("records"):
            lines.append(f"- {row['objection_theme']}: {row['count']} calls. Response angle: {row['suggested_response_angle']}")

    lines.extend(["", "## Deals needing founder attention this week"])
    if deal_rescue_queue.empty:
        lines.append("- No founder rescue queue items generated.")
    else:
        for row in deal_rescue_queue.head(7).to_dict("records"):
            lines.append(f"- {row['priority']}: {row['company_name']} - {row['reason']}")

    lines.extend(["", "## Where the pitch is not landing"])
    if confused.empty:
        lines.append("- No explicit pitch confusion signals were detected.")
    else:
        for row in confused.head(5).to_dict("records"):
            lines.append(f"- {row['company_name']}: {row['pitch_confusion_signals']}")

    lines.extend(
        [
            "",
            "## Narrative changes to test",
            "- Replace broad analytics language with: post-call intelligence for founder-led sales.",
            "- Show the exact outputs: objection bank, deal rescue queue, weekly memo, and narrative experiments.",
            "- Add a competitor framing line: this complements CRMs and call recorders because it turns notes into founder decisions.",
            "- Put proof points near the top: sample memo, sample deal rescue queue, and before-after call notes.",
            "",
            "## Follow-up risks",
        ]
    )
    risk_rows = call_intelligence[call_intelligence["risk_flags"].str.contains("Next step needs tightening|Time-sensitive follow-up", regex=True)]
    if risk_rows.empty:
        lines.append("- No immediate follow-up risks detected.")
    else:
        for row in risk_rows.head(7).to_dict("records"):
            lines.append(f"- {row['company_name']}: {row['risk_flags']}")

    lines.extend(
        [
            "",
            "## Recommended next 7-day actions",
            "- Rescue the highest-priority deals before the next pipeline review.",
            "- Rewrite the pitch around post-call founder learning and deal rescue.",
            "- Add one proof point for security, ROI, integrations, or competitor comparison depending on the top objection.",
            "- Run the same system again next Friday and compare whether objections shift.",
            "- Feed the top three learnings back into CRM notes, sales deck, and founder follow-up messages.",
            "",
        ]
    )
    return "\n".join(lines)
