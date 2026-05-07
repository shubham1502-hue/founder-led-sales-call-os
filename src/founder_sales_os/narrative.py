from __future__ import annotations

from pathlib import Path

import pandas as pd

from founder_sales_os.utils import split_joined


def generate_narrative_experiments(call_intelligence: pd.DataFrame, objection_bank: pd.DataFrame, output_path: str | Path) -> str:
    markdown = build_narrative_experiments(call_intelligence, objection_bank)
    Path(output_path).write_text(markdown, encoding="utf-8")
    return markdown


def build_narrative_experiments(call_intelligence: pd.DataFrame, objection_bank: pd.DataFrame) -> str:
    confusion_rows = call_intelligence[call_intelligence["pitch_confusion_signals"] != "None detected"]
    narrative_rows = call_intelligence[call_intelligence["narrative_gaps"] != "None detected"]
    top_objections = objection_bank.head(5).to_dict("records") if not objection_bank.empty else []
    urgent_segments = (
        call_intelligence[call_intelligence["urgency_score"] >= 60]
        .groupby("industry")
        .size()
        .sort_values(ascending=False)
        .head(5)
    )

    lines: list[str] = [
        "# Narrative Experiments",
        "",
        "This file turns what prospects actually said into messaging tests for the next week.",
        "",
        "## What prospects did not understand",
    ]
    if confusion_rows.empty:
        lines.append("- No major pitch confusion was detected in the sample calls.")
    else:
        for row in confusion_rows.head(5).to_dict("records"):
            lines.append(f"- {row['company_name']}: {row['pitch_confusion_signals']}")

    lines.extend(["", "## Objections that repeated"])
    if not top_objections:
        lines.append("- No repeated objections detected.")
    else:
        for objection in top_objections:
            lines.append(f"- {objection['objection_theme']}: {objection['count']} calls. Angle: {objection['suggested_response_angle']}")

    lines.extend(["", "## Messaging angles to test"])
    lines.extend(build_messaging_angles(top_objections, confusion_rows, narrative_rows))

    lines.extend(["", "## Segments showing strongest urgency"])
    if urgent_segments.empty:
        lines.append("- No segment had clear urgency this week.")
    else:
        for industry, count in urgent_segments.items():
            lines.append(f"- {industry}: {count} urgent or medium-urgency calls")

    lines.extend(["", "## Proof points we need to add"])
    proof_points = collect_proof_points(objection_bank, narrative_rows)
    for point in proof_points:
        lines.append(f"- {point}")

    lines.extend(["", "## Questions the founder should ask in the next 5 calls"])
    lines.extend(
        [
            "- What happens if this same objection shows up in five more calls this month?",
            "- Which part of our pitch made you compare us to your current CRM, recorder, or spreadsheet?",
            "- Who owns the follow-up risk after a sales call today?",
            "- Which deal would this have helped rescue last month?",
            "- What proof would make this feel like a business priority instead of a workflow improvement?",
        ]
    )

    lines.extend(["", "## Suggested homepage or deck messaging changes"])
    lines.extend(
        [
            "- Lead with post-call founder learning, not analytics.",
            "- Show the before and after: messy notes become objections, risks, rescue actions, and narrative tests.",
            "- Add a visual example of the weekly sales learning memo.",
            "- Add a clear line explaining that this complements CRMs and call recorders instead of replacing them.",
            "- Put deal rescue and repeated objection learning above generic ICP scoring.",
        ]
    )

    lines.extend(["", "## Suggested sales-call discovery questions"])
    lines.extend(
        [
            "- Where do call notes live today after a founder-led sales call?",
            "- Which objections have repeated across the last ten calls?",
            "- Which deals are active but do not have a clean next step?",
            "- What does the founder review before the weekly GTM meeting?",
            "- Which competitor or current workflow does this get compared against?",
            "- What would make this worth acting on this week?",
        ]
    )
    lines.append("")
    return "\n".join(lines)


def build_messaging_angles(top_objections: list[dict], confusion_rows: pd.DataFrame, narrative_rows: pd.DataFrame) -> list[str]:
    lines: list[str] = []
    objection_names = {str(item.get("objection_theme", "")).lower() for item in top_objections}
    if "price" in objection_names or "unclear roi" in objection_names:
        lines.append("- Test a revenue leakage angle: stop losing follow-ups and rescue deals before they stall.")
    if "security" in objection_names:
        lines.append("- Test an offline and anonymized-data angle for sensitive sales notes.")
    if "integrations" in objection_names or "switching cost" in objection_names:
        lines.append("- Test a no-migration angle: export notes from the tools you already use.")
    if not confusion_rows.empty:
        lines.append("- Test a category line: post-call intelligence for founder-led sales, not another CRM.")
    if not narrative_rows.empty:
        lines.append("- Test proof-led messaging with sample memos, objection banks, and deal rescue queues.")
    if not lines:
        lines.append("- Test a weekly learning loop angle around five calls, five objections, and one narrative change.")
    return lines


def collect_proof_points(objection_bank: pd.DataFrame, narrative_rows: pd.DataFrame) -> list[str]:
    points: list[str] = []
    if not objection_bank.empty:
        for row in objection_bank.head(4).to_dict("records"):
            points.append(str(row.get("recommended_proof_point")))
    gap_to_proof = {
        "proof": "Add one anonymized raw-note to output example.",
        "roi": "Add a simple ROI example showing founder time saved and pipeline rescued.",
        "workflow": "Add a short diagram of the Friday export to weekly memo workflow.",
        "example": "Add a concrete sample call note and the exact extracted output.",
        "case study": "Add a lightweight case-style walkthrough using synthetic data.",
        "before and after": "Add a before and after view: messy notes on the left, founder decisions on the right.",
        "category": "Add a category explanation: post-call intelligence for founder-led sales.",
        "positioning": "Add a positioning slide that contrasts post-call learning with CRM storage and call recording.",
        "why now": "Add why-now copy tied to board meetings, pipeline reviews, and stalled deals.",
        "who owns this": "Add a section clarifying whether the founder, RevOps, or founder's office owns the weekly loop.",
    }
    for row in narrative_rows.head(5).to_dict("records"):
        for gap in split_joined(row.get("narrative_gaps")):
            normalized_gap = gap.lower().strip()
            point = gap_to_proof.get(normalized_gap)
            if point:
                points.append(point)
    unique: list[str] = []
    seen: set[str] = set()
    for point in points or ["A concrete call-to-output example from raw notes to weekly memo."]:
        if point and point not in seen:
            seen.add(point)
            unique.append(point)
    return unique
