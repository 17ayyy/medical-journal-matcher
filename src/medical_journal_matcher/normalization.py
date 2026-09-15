from __future__ import annotations

import re

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)
ISSN_RE = re.compile(r"^(?P<body>\d{4})-?(?P<tail>\d{3}[\dXx])$")


def normalize_doi(value: str) -> str:
    normalized = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix) :].strip()
            break
    return normalized.rstrip(".,;)")


def is_doi_syntax_valid(value: str) -> bool:
    """Check syntax only; DOI resolvability requires a separate online verification."""
    return DOI_RE.fullmatch(normalize_doi(value)) is not None


def normalize_issn(value: str) -> str:
    match = ISSN_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid ISSN syntax: {value!r}")
    return f"{match.group('body')}-{match.group('tail').upper()}"


def is_issn_checksum_valid(value: str) -> bool:
    try:
        compact = normalize_issn(value).replace("-", "")
    except ValueError:
        return False
    digits = [10 if char == "X" else int(char) for char in compact]
    checksum = sum(weight * digit for weight, digit in zip(range(8, 0, -1), digits, strict=True))
    return checksum % 11 == 0
