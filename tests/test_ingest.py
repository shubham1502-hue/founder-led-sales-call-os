from pathlib import Path

import pandas as pd
import pytest

from founder_sales_os.config import load_company_profile, load_scoring_rules
from founder_sales_os.ingest import IngestError, REQUIRED_COLUMNS, read_sales_calls, validate_sales_calls


ROOT = Path(__file__).resolve().parents[1]


def test_read_sales_calls_sample_csv() -> None:
    df = read_sales_calls(ROOT / "data/sample_sales_calls.csv")

    assert len(df) >= 15
    assert list(REQUIRED_COLUMNS) == [column for column in REQUIRED_COLUMNS if column in df.columns]
    assert pd.api.types.is_integer_dtype(df["employee_count"])


def test_required_column_validation() -> None:
    df = pd.DataFrame({"call_id": ["CALL-001"]})

    with pytest.raises(IngestError, match="missing required columns"):
        validate_sales_calls(df)


def test_config_loading() -> None:
    company_profile = load_company_profile(ROOT / "config/company_profile.yml")
    scoring_rules = load_scoring_rules(ROOT / "config/scoring_rules.yml")

    assert company_profile["product_name"] == "Founder-Led Sales Call OS"
    assert "icp_fit" in scoring_rules
