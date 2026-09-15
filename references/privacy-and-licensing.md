# Privacy and licensing

## Trust boundary

`LOCAL_PARSE_ONLY` is the default. Full manuscripts are read only by deterministic processes in the user's controlled workspace. External scholarly services receive only a structured query made from an allowlist:

- topics, diseases, and biological processes;
- population or research object;
- submission format and study designs;
- methods, techniques, or imaging modalities;
- normalized outcome/contribution categories without unpublished exact values;
- MeSH terms and necessary synonyms.

Never transmit original title/abstract/body sentences, author identity, affiliation, email, funding, acknowledgements, conflicts, patient identifiers, rare identifying combinations, or unpublished exact results. Apply a field allowlist; free-text "redaction" is not sufficient. Preview the outbound query before the first request in full-manuscript mode.

`MODEL_ASSISTED_WITH_CONSENT` requires run-specific consent that records recipient, purpose, allowed content, retention notice, and time. Scholarly search APIs still must not receive manuscript text. `OFFLINE_ONLY` makes no external request; if local data cannot establish freshness or provenance, report the limitation instead of completing a formal recommendation.

Readiness findings leaving the local parser are limited to check ID, category, severity, status, evidence location, short observed/expected values, rule ID, and limitation. Qualitative language, narrative, or statistical judgment is `NOT_ASSESSED` unless a declared trusted local model or explicit consent is available.

## Licensing and retention

- JCR/JIF are licensed data. Use Clarivate or an authorized user import; never infer or replace them.
- Respect API rate limits, attribution, caching, and redistribution terms.
- Store only minimal factual metadata needed for the run.
- Do not retain copyrighted abstracts/full text or unclear-license content.
- Logs, caches, exceptions, reports, and version control must not contain manuscript text or credentials.
