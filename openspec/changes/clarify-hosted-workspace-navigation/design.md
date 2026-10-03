# Design

Pipeline reads the same candidate-scoped VPS opportunity collection as Search, refreshes on mount, window focus and every ten seconds, and exposes manual refresh and text filtering. Applications retains existing tracker semantics. Recovery and archived snapshot labels explain where search history and saved jobs live. No canonical tracker or pipeline content is rewritten by the navigation change.

A bounded fixed-job deployment helper records the owner-stated Grafana note in Brad's private data/opportunity-notes.json, under shared locking with a previous-version checkpoint. Notes are idempotent, attributed to the user statement, exported/backed up with candidate documents, and displayed on the pipeline card. No notes are copied into CV/profile claims.

Activate only an exact versioned release with matching source hashes/build IDs. Owner sudo remains necessary; no Caddy change. Rollback keeps data and user notes.
