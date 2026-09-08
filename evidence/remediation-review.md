# Ten-minute demonstration verification

Current contract: 0x48B8995384E8340892554567965aA5910c69B380. Only the sanshos1 wallet may sign this project's live tests.

| Reviewer requirement | Verification | Status |
|---|---|---|
| Delayed scoring preserves a post-score appeal window | Direct VM scoring two days late stores a fresh 600-second window | PASS |
| Appeal remains possible through exact deadline | Boundary test permits appeal and rejects finalization at the exact deadline | PASS |
| Permissionless completion strictly after deadline | Synthetic other-caller direct VM test | PASS (local) |
| Longer requested deadline is preserved | Direct VM test keeps the longer requested date | PASS |
| Code passes GenVM lint | Three checks pass | PASS |
| Actual deployment source matches reviewed code | owner-network.json sourceMatches and SHA-256 | PASS |
| New live lifecycle and early-finalization rejection | owner-network.json, in progress | UNVERIFIED |
| Published UI reads new deployment | Pending published build check | UNVERIFIED |

Seven direct VM tests pass. The 600-second minimum is an explicitly requested StudioNet demonstration setting; a reviewer may require a longer practical window. Multi-account wallets are never used. Retired deployments' results are not evidence for this address.
