# Merit Circuit resubmission

Update the submission through Edit before resubmitting. Replace earlier contract links with this deployment.

## What did you change? (818 characters)

Fixed the delayed-scoring appeal bug: scoring starts a fresh minimum appeal window, while preserving any later requested deadline. This StudioNet demonstration uses 600 seconds (10 minutes), explicitly shown in the UI. The subject can appeal through the exact deadline; permissionless finalization is allowed only afterward. Seven direct VM tests pass, including delayed scoring, boundary behavior and preservation of longer deadlines. The deployed source matches the reviewed code. On the new deployment, MC-OWNER-1788879441 completed scoring, appeal and finalization; an early-finalization transaction was rejected by the appeal guard. All live test transactions used only the project owner's wallet. The public workbench reads the FINAL record. Please use the updated contract link; earlier deployments are retired.

## Website

https://sanshos1.github.io/merit-circuit/

## GitHub

https://github.com/sanshos1/merit-circuit

## Contract evidence

https://explorer-studio.genlayer.com/address/0x48B8995384E8340892554567965aA5910c69B380

## Finalization transaction evidence

https://explorer-studio.genlayer.com/tx/0x4246493d92e78e70e1c5a4041236b871a8d15239feb968f8c1de262252f4e58d

## Reviewer path

Open the website, enter MC-OWNER-1788879441 under Epoch reference, then choose LOAD EPOCH. The recorded result is FINAL, score 85, with QUALITY 50 and ADOPTION 35. Inspect the stored sources, appeal record and three digests.

## Scope

The live transaction lifecycle was verified using the SDK; the public browser verification covered reading the final state. The ten-minute minimum is explicitly a StudioNet demonstration setting. All real signing used only sanshos1's wallet. This file describes Merit Circuit only and does not claim Guild Passport has a new completed live lifecycle.
