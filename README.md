# Merit Circuit

## Current remediation status

Local correction: scoring grants at least 86,400 seconds from the scoring timestamp, even when the creation-time deadline has expired. A later requested deadline is preserved. Appeals are allowed through the deadline and permissionless finalization starts strictly afterward. Regression tests cover delayed scoring, the exact boundary, subject-only appeal and finalization by another caller. Earlier deployment/lifecycle records below are historical and do not verify this correction. See `evidence/remediation-review.md` before resubmission.

Merit Circuit creates evidence-weighted reputation epochs instead of permanent opaque scores. Every epoch stores two operator-configured, distinct-host base evidence URLs. Validators apply one immutable rubric: QUALITY is capped at 60 and ADOPTION at 40, and they verify both exact component values and the total.

Scoring opens an enforceable appeal window. The subject alone may file evidence from a third host before the stored deadline, and nobody can finalize before that deadline. Afterward finalization is permissionless, preventing abandonment. Duplicate IDs, source reuse, malformed URLs, rubric drift, early finalization, unauthorized appeals and forged components are tested. Run `python -m pytest score_tests -q`.

Verified StudioNet deployment: `0xf1C61C7ef26904e2C390Af3F0eCDcDa0046a5f8d`, source commit `c77f201118a2f818b29443186d5e45d3eb8b01f7`. The recorded live lifecycle proves early finalization rejection, subject appeal acceptance, post-deadline finalization and exact 60/40 rubric output.
