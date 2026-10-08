# Verification

Implementation is authorized; release activation remains owner-run.

Local tests cover reviewed registration, unchanged primary CV, canonical numbered report/JD, Evaluated-only status, initial status ledger, immutable original review, backup, idempotency and duplicate posting refusal. Fault injection exercises write-ahead replay and refusal after unrelated tracker changes. Canonical tracker-lock contention is tested against another process; automatic backup refuses pending registration journals. Candidate-bound IDs, symlink escapes, stale quality/evidence fingerprints, exact resume extraction, unavailable check coverage and inert external HTML/image text are tested.

Production build, fictional browser flow and rendered PDF inspection results will be recorded before staging the activation handoff. No production candidate documents are created for qualification.
