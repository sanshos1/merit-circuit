# Merit Circuit

Merit Circuit creates evidence-weighted reputation epochs instead of permanent opaque scores. Every epoch stores two operator-configured, distinct-host base evidence URLs. Validators apply one immutable rubric: QUALITY is capped at 60 and ADOPTION at 40, and they verify both exact component values and the total.

Scoring opens an enforceable appeal window. The subject alone may file evidence from a third host before the stored deadline, and nobody can finalize before that deadline. Afterward finalization is permissionless, preventing abandonment. Duplicate IDs, source reuse, malformed URLs, rubric drift, early finalization, unauthorized appeals and forged components are tested. Run `python -m pytest score_tests -q`.
