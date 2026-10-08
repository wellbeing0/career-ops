# Verification

Seventeen portal Python tests pass, syntax checks pass and OpenSpec validates strictly. Both candidate web bundles rebuilt successfully. The first build attempts encountered dependency symlink restrictions; an independent dependency copy and direct Next build entrypoint resolved them without configuration changes.

Browser checks passed for phone 390×700 and desktop 1280×900, light/dark themes, two top workspace links, six workflow steps, eight feature definitions and no horizontal overflow or browser errors. The first two workflow cards are visible within the phone viewport. Both rebuilt workspaces render the root Job-search guide link and no archive-index header link, using fictional API fixtures for bounded UI testing. Phone and desktop screenshots were visually reviewed.

All 177 other static files are byte-identical to the previous release. Only the two candidate static archive index pages were removed. All 46 Brad and 42 Steve archive entries from the real authenticated live document catalogs still resolve to staged original files. Candidate data and the live library archive indexes are unchanged.

Updated Assistant guides, source hashes, both build IDs and the static manifest are sealed in the staged `20261008-compact-guide-01` qualification receipt. Prior release remains recoverable. Owner activation and live acceptance are pending:

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261008-compact-guide-01/portal/deploy/activate-compact-guide.py
```

The same helper with `--rollback` restores the previous code and static release.
