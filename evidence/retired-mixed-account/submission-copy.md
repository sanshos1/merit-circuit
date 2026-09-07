# Merit Circuit submission draft

Do not resubmit before the recorded live epoch reaches FINAL and the manifest is updated.

## Project name

Merit Circuit: Evidence-Weighted Contribution Review

## One-liner

A source-bound contribution scoring workflow with validator-checked rubric values and a guaranteed post-score appeal period.

## Description

Merit Circuit turns contribution review into an auditable GenLayer lifecycle. Each epoch fixes a subject, scope and two configurable HTTPS evidence sources on distinct hosts. Validators retrieve the evidence and verify the exact QUALITY and ADOPTION components, their caps and the stored total. Scoring opens at least 24 hours for the subject to add appeal evidence, even when scoring happens after the originally requested date. Appeals are accepted through the stored boundary, and anyone may finalize only after it. Finalization re-evaluates an appealed epoch with the original and appeal records. Duplicate IDs, reused hosts, invalid rubric output, forged components, unauthorized appeals and early finalization are rejected. The public workbench reads the corrected StudioNet deployment and exposes the complete lifecycle without hardcoded results.

## Exact path

1. Open the public workbench.
2. Enter MC-1788806858 under Epoch reference.
3. Select LOAD EPOCH to inspect the live score, evidence sources, appeal record and stored deadline.
4. For a fresh epoch, connect a StudioNet wallet, enter a unique ID, your wallet as subject, a scope, two HTTPS source URLs on distinct hosts and a future requested date.
5. Register the epoch, issue the score, load the stored deadline, file an appeal from the subject wallet if needed, then seal the ledger only after that deadline.

## Expected verification outcome

The recorded epoch currently displays APPEALED, score 85, two stored source slots and appeal deadline 1788893290. After the deadline and final live test, it must display FINAL. Early finalization must fail. A fresh score must store a deadline at least 86,400 seconds after scoring.

## Website

https://sanshos1.github.io/merit-circuit/

## GitHub repository

https://github.com/sanshos1/merit-circuit

## GenLayer Explorer contract

https://explorer-studio.genlayer.com/address/0x785754092A73fD9d0274b0a751449EdE47b4bf0a
