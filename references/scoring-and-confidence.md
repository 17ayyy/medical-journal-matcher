# Scoring, confidence, and tiers

All numbers come from deterministic, versioned features in `config/scoring.v0.1.0.toml`. A model may extract labels or explain evidence but does not choose final numeric scores.

## Match score

The 100 points are: scope 30, methods/design 20, population/object 10, recent articles 25, audience/positioning 10, and soft preferences 5. Each atomic feature is a 0–1 value or `null`.

- `0` means adequate evidence of non-match.
- `null` means unavailable or not assessable.
- `assessed_weight` is the sum of weights for non-null features.
- `raw_weighted_points` is the weighted sum.
- `final_match_score = raw_weighted_points / assessed_weight * 100`.
- `score_coverage = assessed_weight / 100`.

Formal eligibility requires all enabled hard gates `PASS`, score at least 65.0, coverage at least 0.80, confidence at least `MEDIUM`, and 1–5 valid articles within the recent three-year window.

Do not infer official scope from a journal title. Retrieval failure is `null`; successful sufficient retrieval with no match is `0`. Speed subweights are fixed at 1.2/0.9/0.6/0.3 and are never redistributed.

## Confidence

Compute a 0–1 weighted score from input sufficiency 15%, evidence sufficiency 25%, provenance completeness 25%, signal agreement 15%, stability 10%, and freshness 10%.

1. Any enabled gate `FAIL` or `UNVERIFIED` forces `LOW`.
2. Otherwise score at least 0.80 with every component at least 0.50 is `HIGH`.
3. Otherwise score at least 0.60 is `MEDIUM`; lower is `LOW`.

Evidence sufficiency is 1.0 for at least three valid DOI articles from at least two teams/issues, 0.67 for two, 0.33 for one, and 0 for none. Round the aggregate to two decimals and store the scoring version.

## Strategy tiers

Build an eligible pool first. Compute journal position from licensed manuscript-relevant JCR categories; use the least favorable passing category position under the configured ANY/ALL policy. Split comparable positions into thirds while keeping boundary ties together.

- `SPRINT`: high position, match score at least 75, confidence at least medium.
- `RELATIVELY_SAFE`: lower position, match at least 65, recent-article subscore at least 0.60, scope breadth at least 0.60.
- `PRIORITY`: other formally eligible candidates, including eligible candidates without comparable position data.

If JCR position is not legally available/comparable, output only `PRIORITY`; never fabricate the other tiers. Internal ordering is deterministic: score descending, confidence, coverage, recent-evidence score, DOI count, then normalized title ascending.
