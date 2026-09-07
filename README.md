# Merit Circuit

Evidence-weighted contribution epochs with an enforceable subject appeal window.

## Current reviewed deployment

- StudioNet: [contract](https://explorer-studio.genlayer.com/address/0x785754092A73fD9d0274b0a751449EdE47b4bf0a).
- Contract source commit: c97f9a6d5278d265e71c56db227527826a82f8de.
- [Public workbench](https://sanshos1.github.io/merit-circuit/).
- Actual deployment transaction code matches the reviewed source; see evidence/deployment-verification.json. Earlier network-run.json is historical.

## Rules and consensus

An epoch fixes its subject, scope and two configurable HTTPS source URLs on distinct hosts. Distinct hosts do not prove independent ownership. Validators recheck the evidence and exact QUALITY (0–60), ADOPTION (0–40), and total scores. The subject can submit appeal evidence from a third host. Scoring always extends the appeal deadline to at least 86,400 seconds after scoring; a later requested deadline is preserved. Appeals are allowed at the deadline; permissionless finalization is allowed only strictly afterward.

## Reproduce

Open the workbench and enter MC-1788806858, then LOAD EPOCH for the actual remediation record. It is APPEALED; the protected deadline is 2026-09-08 18:48:10 UTC. Post-deadline live finalization is pending, not passed.

For a fresh workflow, connect a StudioNet wallet through MetaMask or Rabby. Enter a unique epoch ID, subject address, scope, two actual source URLs and a future requested date. Register, score, load the returned deadline, switch to the subject wallet to appeal, and finalize only after that stored deadline. Keep the same epoch ID when switching roles. Wallet transactions require network fees and the required role.

The shipped UI is a static ES-module application in docs/; no build step is required. Serve that directory over HTTP. Its pinned SDK is loaded from esm.sh. Run python -m pytest score_tests -q and genvm-lint scoring_engine/merit_circuit.py (set PYTHONIOENCODING=utf-8 on Windows).

## Evidence and limits

Six direct VM tests pass, including delayed scoring, boundary behavior and unauthorized actions. Real delayed scoring, early-finalization rejection, unauthorized-appeal rejection and subject appeal are recorded in evidence/remediation-network.json. These scripted tests do not prove a complete browser wallet workflow. See evidence/remediation-review.md for remaining gates. No acceptance guarantee is made.
