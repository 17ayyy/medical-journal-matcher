# Submission taxonomy

Keep the three axes independent:

| User scenario | `submission_format` | Typical `study_designs` | Typical guidelines |
|---|---|---|---|
| Original research | `ORIGINAL_ARTICLE` | `COHORT`, `CASE_CONTROL`, `CROSS_SECTIONAL`, `EXPERIMENTAL` | STROBE, ARRIVE, or applicable guidance |
| Systematic review/meta-analysis | `REVIEW_ARTICLE` | `SYSTEMATIC_REVIEW`, `META_ANALYSIS` | PRISMA |
| Clinical trial | `ORIGINAL_ARTICLE` | `CLINICAL_TRIAL`, optionally `RANDOMIZED_CONTROLLED_TRIAL` | CONSORT |
| Diagnostic accuracy | `ORIGINAL_ARTICLE` | `DIAGNOSTIC_ACCURACY` | STARD |
| Case report/series | `CASE_REPORT` or `CASE_SERIES` | same as format | CARE or applicable guidance |
| Methods paper | `METHODS_ARTICLE` | `METHOD_DEVELOPMENT`, `METHOD_VALIDATION` | domain-specific guidance |

Map official aliases such as Research Article, Original Research, and Original Investigation to the canonical format only when the current author guide supports the mapping. Preserve the original label, source URL, checked date, and mapping confidence. An uncertain or conflicting format mapping is `UNVERIFIED`; ask the user to confirm the intended format before applying this gate.
