from pathlib import Path

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.extraction import extract_call_intelligence
from founder_sales_os.ingest import read_sales_calls


ROOT = Path(__file__).resolve().parents[1]


def load_context():
    return (
        read_sales_calls(ROOT / "data/sample_sales_calls.csv"),
        load_company_profile(ROOT / "config/company_profile.yml"),
        load_scoring_rules(ROOT / "config/scoring_rules.yml"),
    )


def test_objection_extraction_detects_price_and_competitor() -> None:
    df, company_profile, scoring_rules = load_context()
    record = df[df["call_id"] == "CALL-001"].iloc[0].to_dict()

    intelligence = extract_call_intelligence(record, company_profile, scoring_rules)

    assert "Price" in intelligence["extracted_objections"]
    assert "Gong" in intelligence["competitor_mentions"]


def test_urgency_extraction_detects_high_urgency() -> None:
    df, company_profile, scoring_rules = load_context()
    record = df[df["call_id"] == "CALL-006"].iloc[0].to_dict()

    intelligence = extract_call_intelligence(record, company_profile, scoring_rules)

    assert "High urgency" in intelligence["urgency_signals"]
    assert "Time-sensitive follow-up" in intelligence["risk_flags"]


def test_pitch_confusion_extraction() -> None:
    df, company_profile, scoring_rules = load_context()
    record = df[df["call_id"] == "CALL-008"].iloc[0].to_dict()

    intelligence = extract_call_intelligence(record, company_profile, scoring_rules)

    assert intelligence["pitch_confusion_signals"] != "None detected"
    assert "Pitch confusion" in intelligence["risk_flags"]
