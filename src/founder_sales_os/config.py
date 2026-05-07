from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(ValueError):
    """Raised when a YAML config file is missing required founder-facing fields."""


COMPANY_REQUIRED_KEYS = (
    "product_name",
    "target_customer",
    "primary_use_cases",
    "strong_fit_signals",
    "weak_fit_signals",
    "disqualifiers",
    "target_industries",
    "target_company_stages",
    "value_proposition",
    "competitor_keywords",
    "objection_keywords",
    "urgency_keywords",
    "buying_trigger_keywords",
    "confusion_keywords",
    "narrative_gap_keywords",
    "proof_point_keywords",
)

SCORING_REQUIRED_KEYS = (
    "score_boundaries",
    "icp_fit",
    "pain_intensity",
    "budget_signal",
    "follow_up_clarity",
    "pitch_clarity",
    "implementation_risk",
    "deal_rescue_priority",
)


def load_yaml(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"Config file must contain a YAML mapping: {config_path}")
    return data


def require_keys(data: dict[str, Any], keys: tuple[str, ...], path: str | Path) -> None:
    missing = [key for key in keys if key not in data]
    if missing:
        raise ConfigError(f"{path} is missing required keys: {', '.join(missing)}")


def load_company_profile(path: str | Path) -> dict[str, Any]:
    data = load_yaml(path)
    require_keys(data, COMPANY_REQUIRED_KEYS, path)
    return data


def load_scoring_rules(path: str | Path) -> dict[str, Any]:
    data = load_yaml(path)
    require_keys(data, SCORING_REQUIRED_KEYS, path)
    return data
