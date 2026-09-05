# Merit Circuit

Merit Circuit creates evidence-weighted reputation epochs instead of permanent opaque scores. A maintainer opens an epoch for a subject; validators verify the exact 0 to 100 score and every component point. The subject may add distinct appeal evidence before finalization.

Components must sum exactly to the stored score. Duplicate IDs, source reuse, unauthorized appeals, forged scores and repeat transitions are rejected. Run `python -m pytest -q` and `genvm-lint contract/merit_circuit.py`.
