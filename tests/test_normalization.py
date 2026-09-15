import pytest

from medical_journal_matcher.normalization import (
    is_doi_syntax_valid,
    is_issn_checksum_valid,
    normalize_doi,
    normalize_issn,
)


def test_doi_normalization_is_lowercase_without_url() -> None:
    assert normalize_doi("https://doi.org/10.1000/ABC.1") == "10.1000/abc.1"
    assert is_doi_syntax_valid("doi:10.1000/ABC.1")


def test_issn_normalization_and_checksum() -> None:
    assert normalize_issn("2049-3630") == "2049-3630"
    assert is_issn_checksum_valid("2049-3630")
    with pytest.raises(ValueError):
        normalize_issn("not-an-issn")
