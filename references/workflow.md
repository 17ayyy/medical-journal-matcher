# Workflow

This file is the operational companion to PRD sections 9, 11, 17, 21, 23, and 26.

## Intake

Reuse the title, abstract, keywords, manuscript, specialty, and constraints already supplied. Establish:

1. input sufficiency;
2. primary domain and specialties;
3. `submission_format`, multi-label `study_designs`, and `reporting_guidelines`;
4. required WoS indexes (default `SCIE`);
5. target JCR quartiles and confirmed manuscript-relevant categories;
6. OA requirement;
7. publication-speed and publisher preferences;
8. optional preferred/excluded journals, excluded publishers, APC budget, and tier counts;
9. JCR data mode and privacy mode.

Pause only for ambiguity in a hard constraint. Soft preferences may use an explicit default. Before retrieval, show a short profile and constraint summary, including JCR and privacy modes.

## Pipeline

`intake -> local parse -> manuscript profile -> outbound query preview -> article retrieval -> candidate aggregation -> journal identity normalization -> source verification -> hard gates -> deterministic scoring -> confidence -> tiering -> readiness -> report`

Candidate sources are recent real publishing venues, official scope matches, and user seeds. Respect all explicit exclusions. Normalize journals by ISSN-L, pISSN/eISSN, title history, and publisher identity.

For each enabled gate record `PASS`, `FAIL`, `UNVERIFIED`, or `NOT_APPLICABLE` with Chinese reason and evidence references. A single `FAIL` excludes a journal. No `FAIL` plus any `UNVERIFIED` sends it to the unverified list. Only all-`PASS` candidates may be evaluated for formal tiers.

## Degraded public-JCR flow

When no licensed or authorized user JCR data is available:

- set `jcr_data_mode=PUBLIC`;
- never substitute CiteScore, SJR, or another metric for JIF/JCR;
- set the JCR gate to `UNVERIFIED`;
- leave formal recommendation tiers empty;
- return content-fit candidates under a title that clearly says JCR verification is incomplete;
- allow a later authorized JCR CSV/XLSX import to resume gating and tiering.

## Report order

1. Conclusion summary.
2. Input and constraint recap.
3. Manuscript Profile.
4. JCR/privacy mode, query date, and limitations.
5. Three-tier summary table.
6. Detailed journal cards.
7. Unverified candidates.
8. Excluded candidates and reasons.
9. Submission Readiness Audit when applicable.
10. Sources, disclaimer, and manual checks.

If a tier has no eligible journals, keep it empty and state why. Never fill quotas by weakening constraints or using stale/invalid article evidence.
