from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = (
    "call_id",
    "call_date",
    "company_name",
    "contact_role",
    "company_stage",
    "employee_count",
    "industry",
    "lead_source",
    "call_notes",
    "current_tooling",
    "stated_pain",
    "budget_signal",
    "timeline_signal",
    "next_step",
    "deal_stage",
)


class IngestError(ValueError):
    """Raised when input call data cannot be used by the OS."""


def read_sales_calls(path: str | Path) -> pd.DataFrame:
    csv_path = Path(path)
    if not csv_path.exists():
        raise IngestError(f"Input CSV not found: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception as exc:
        raise IngestError(f"Could not read input CSV {csv_path}: {exc}") from exc

    validate_sales_calls(df, csv_path)
    cleaned = df.copy()
    cleaned["employee_count"] = pd.to_numeric(cleaned["employee_count"], errors="raise").astype(int)
    cleaned["call_date"] = pd.to_datetime(cleaned["call_date"], errors="raise").dt.strftime("%Y-%m-%d")
    return cleaned


def validate_sales_calls(df: pd.DataFrame, source: str | Path = "input CSV") -> None:
    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise IngestError(f"{source} is missing required columns: {', '.join(missing)}")
    if df.empty:
        raise IngestError(f"{source} has no sales call rows")

    duplicate_ids = df["call_id"][df["call_id"].duplicated()].tolist()
    if duplicate_ids:
        raise IngestError(f"{source} has duplicate call_id values: {', '.join(map(str, duplicate_ids))}")

    blank_required: list[str] = []
    for column in REQUIRED_COLUMNS:
        if df[column].isna().any() or (df[column].astype(str).str.strip() == "").any():
            blank_required.append(column)
    if blank_required:
        raise IngestError(f"{source} has blank values in required columns: {', '.join(blank_required)}")
