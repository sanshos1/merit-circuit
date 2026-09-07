# Merit Circuit

## Current replacement deployment

- Owner: sanshos1; signing wallet: 0xAD049E0Edc298C97552eD60071a35bfc60181FD4.
- StudioNet contract: [0x79aAC36e444cDa73b845AE5129574Ea32e0ce7b5](https://explorer-studio.genlayer.com/address/0x79aAC36e444cDa73b845AE5129574Ea32e0ce7b5).
- [Public application](https://sanshos1.github.io/merit-circuit/).
- Deployment and actual-source verification: evidence/deployment.json and evidence/owner-network.json.

New owner-only record MC-OWNER-1788810754 is APPEALED. Its creator and subject are both the sanshos1 wallet. Post-deadline finalization remains pending.

## Account isolation

Only ACCOUNT_3 may sign for this repository. The deployment helper validates its derived address before any transaction. Old smoke scripts are disabled. Each account's projects use only that account's wallet. Multi-party roles are tested locally using synthetic addresses, without reading keys from other accounts. Contract authorization rules remain enforced.

Earlier mixed-account deployments are retired. Historical proofs in evidence/retired-mixed-account and prior Git commits are not results for this new address. The earlier finalization automation is paused.

## Contract behavior

An epoch fixes its subject, scope and two configurable HTTPS evidence URLs. Validators check exact QUALITY (0-60), ADOPTION (0-40) and total values. Scoring grants at least 24 hours for the subject to appeal, even after a delayed score. Appeals are allowed through the stored deadline; finalization is permissionless strictly afterward. An appealed epoch is re-evaluated with its appeal evidence. Distinct source hosts alone do not prove independent ownership.

## Verification and use

Enter MC-OWNER-1788810754 and select LOAD EPOCH to read the new test.

Run python -m pytest score_tests -q for local tests, genvm-lint scoring_engine/merit_circuit.py for lint, and python epoch_ops/owner_smoke.py for the owner-only check. The Merit check performs owner-only writes and resumes finalization only after the stored deadline.

The website is a static ES-module application served from docs/ with its SDK pinned to genlayer-js 1.1.8. Wallet writes need a supported StudioNet browser wallet. Reading the public app does not require one. See evidence/remediation-review.md for remaining verification.
