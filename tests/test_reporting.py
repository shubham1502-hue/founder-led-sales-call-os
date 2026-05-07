from pathlib import Path

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.ingest import read_sales_calls
from founder_sales_os.reporting import CALL_INTELLIGENCE_COLUMNS, run_pipeline


ROOT = Path(__file__).resolve().parents[1]


def test_report_generation(tmp_path: Path) -> None:
    sales_calls = read_sales_calls(ROOT / "data/sample_sales_calls.csv")
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")

    paths = run_pipeline(sales_calls, company_profile, scoring_rules, tmp_path)

    for path in paths.values():
        assert path.exists()

    call_intelligence = paths["call_intelligence"].read_text(encoding="utf-8")
    memo = paths["weekly_sales_learning_memo"].read_text(encoding="utf-8")

    assert "call_id" in call_intelligence
    assert "Weekly Sales Learning Memo" in memo
    assert "deal_rescue_priority_score" in CALL_INTELLIGENCE_COLUMNS
