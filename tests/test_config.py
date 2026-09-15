from medical_journal_matcher.config import JcrDataMode, PrivacyMode, Settings


def test_safe_defaults() -> None:
    settings = Settings(_env_file=None)
    assert settings.journal_matcher_jcr_data_mode is JcrDataMode.PUBLIC
    assert settings.journal_matcher_privacy_mode is PrivacyMode.LOCAL_PARSE_ONLY
