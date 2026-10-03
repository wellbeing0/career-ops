# Live Documents release

After qualification, activate with:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-documents-01/portal/deploy/activate-documents.py
```

Open each workspace and select Documents. Current files are inventoried directly on the authoritative VPS; new search reports and saved application documents appear on refresh, focus or the 30-second refresh. No daily document publishing process is needed. The dated static snapshot remains available as Archive, with source, type, date and text filters. The activation verifies and indexes existing archive originals without replacing candidate files.

Current text can be previewed safely; binary files and text over 1 MB can be downloaded. Private runtime, backups, secrets, nested checkouts and linked files are excluded. Profile and CV editing and automatic prior-version history remain in their existing tabs.

Rollback code and service definitions if needed:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-documents-01/portal/deploy/activate-documents.py --rollback
```

Candidate documents, searches, history and archive metadata are retained on rollback. AI integration is a subsequent planned phase, not enabled by this release.
