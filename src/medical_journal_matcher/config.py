from __future__ import annotations

from enum import StrEnum

from pydantic_settings import BaseSettings, SettingsConfigDict


class JcrDataMode(StrEnum):
    LICENSED_JCR = "LICENSED_JCR"
    USER_JCR_IMPORT = "USER_JCR_IMPORT"
    PUBLIC = "PUBLIC"


class PrivacyMode(StrEnum):
    LOCAL_PARSE_ONLY = "LOCAL_PARSE_ONLY"
    MODEL_ASSISTED_WITH_CONSENT = "MODEL_ASSISTED_WITH_CONSENT"
    OFFLINE_ONLY = "OFFLINE_ONLY"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    journal_matcher_jcr_data_mode: JcrDataMode = JcrDataMode.PUBLIC
    journal_matcher_privacy_mode: PrivacyMode = PrivacyMode.LOCAL_PARSE_ONLY
    journal_matcher_log_level: str = "INFO"
    clarivate_api_key: str | None = None
    openalex_api_key: str | None = None
    ncbi_api_key: str | None = None
    crossref_contact_email: str | None = None
    unpaywall_contact_email: str | None = None
