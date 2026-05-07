from __future__ import annotations

from collections.abc import Iterable, Mapping
import math
import re
from typing import Any


TEXT_FIELDS = (
    "call_notes",
    "current_tooling",
    "stated_pain",
    "budget_signal",
    "timeline_signal",
    "next_step",
    "deal_stage",
    "contact_role",
    "company_stage",
    "industry",
)


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    return str(value).strip()


def normalize_text(value: Any) -> str:
    text = coerce_text(value).lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def text_blob(record: Mapping[str, Any], fields: Iterable[str] = TEXT_FIELDS) -> str:
    return " ".join(coerce_text(record.get(field, "")) for field in fields)


def normalize_keyword_groups(value: Any) -> dict[str, list[str]]:
    if isinstance(value, Mapping):
        return {str(key): [coerce_text(item) for item in values] for key, values in value.items()}
    if isinstance(value, list):
        return {"signals": [coerce_text(item) for item in value]}
    return {}


def unique_preserve(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = coerce_text(value)
        if not clean:
            continue
        key = clean.lower()
        if key not in seen:
            seen.add(key)
            result.append(clean)
    return result


def keyword_present(text: str, keyword: str) -> bool:
    clean_text = normalize_text(text)
    clean_keyword = normalize_text(keyword)
    if not clean_keyword:
        return False
    return clean_keyword in clean_text


def find_keywords(text: str, keywords: Iterable[str]) -> list[str]:
    return unique_preserve(keyword for keyword in keywords if keyword_present(text, keyword))


def find_group_matches(text: str, groups: Mapping[str, Iterable[str]]) -> dict[str, list[str]]:
    matches: dict[str, list[str]] = {}
    for label, keywords in groups.items():
        found = find_keywords(text, keywords)
        if found:
            matches[label] = found
    return matches


def labels_from_matches(matches: Mapping[str, list[str]]) -> list[str]:
    return [label for label, found in matches.items() if found]


def humanize_label(label: str) -> str:
    return label.replace("_", " ").strip().title()


def join_values(values: Iterable[str], empty: str = "None detected") -> str:
    unique = unique_preserve(values)
    return "; ".join(unique) if unique else empty


def split_joined(value: Any) -> list[str]:
    text = coerce_text(value)
    if not text or text.lower() == "none detected":
        return []
    return [part.strip() for part in text.split(";") if part.strip()]


def first_sentence(text: Any, max_chars: int = 180) -> str:
    clean = coerce_text(text)
    if not clean:
        return ""
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0]
    if len(sentence) <= max_chars:
        return sentence
    return sentence[: max_chars - 3].rstrip() + "..."


def clamp_score(value: float, minimum: int = 0, maximum: int = 100) -> int:
    return max(minimum, min(maximum, int(round(value))))


def any_keyword(text: str, keywords: Iterable[str]) -> bool:
    return bool(find_keywords(text, keywords))


def count_group_matches(text: str, groups: Mapping[str, Iterable[str]]) -> int:
    return sum(len(matches) for matches in find_group_matches(text, groups).values())


def role_is_decision_maker(role: Any) -> bool:
    clean = normalize_text(role)
    return any(
        term in clean
        for term in (
            "founder",
            "cofounder",
            "ceo",
            "owner",
            "president",
            "vp",
            "head of",
            "chief",
            "cro",
            "coo",
        )
    )
