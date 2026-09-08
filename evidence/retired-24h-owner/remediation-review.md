# Replacement deployment verification

| Check | Status | Evidence |
|---|---|---|
| Only project-owner wallet signs | PASS | epoch_ops/owner_wallet.py checks ACCOUNT_3 derived address; owner-network.json records signer |
| Fresh replacement deployed by sanshos1 | PASS | deployment.json, owner-network.json |
| Actual deployed source matches local contract | PASS | base64 deployment source compared byte-for-byte after deployment text normalization |
| Old mixed-account smoke scripts disabled | PASS | smoke.py and remediation_smoke.py exit before loading credentials |
| Local role and reviewer regression tests | PASS (previous contract tests; contract source unchanged) | 6 direct VM tests using synthetic addresses |
| New live lifecycle | PARTIAL: APPEALED, deadline pending | owner-network.json |
| Public frontend reads replacement | PASS (read only) | Published website returned MC-OWNER-1788810754, APPEALED, score 85, deadline 1788897162 |
| Fresh browser wallet lifecycle | UNVERIFIED | No wallet provider in controlled browser |

The old deployment proofs do not apply to this replacement. Do not submit old Explorer links or claim its records exist at the new address.
