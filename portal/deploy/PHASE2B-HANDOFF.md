# Phase 2B: free browser search

Implementation is approved. Release `20261003-search-01` is prepared for activation only after its qualification receipt and exact source/build hashes are present. This is a code update; the VPS remains authoritative.

## Activate on the VPS

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-search-01/portal/deploy/activate-search.py
```

The helper verifies qualified source hashes and both build IDs, switches the two editor code paths, updates backup helper paths, and restarts the editors with startup checks. It retains shared login, candidate roots, history, Caddy routing and already-enabled backup timers. Private previous definitions are stored under `/etc/career-ops/search-activation-20261003-01.json`, mode 0600; never copy or print that file because it contains environment definitions.

No additional Caddy configuration is needed: existing authenticated workspace routes already reach the proxy's narrow allowlist. The only newly allowed API is `/api/hosted/search`; generic workers, discovery, submission and other upstream APIs stay blocked.

## Use on a phone

Open your live workspace and tap **Search**, then **Start free search**. You can close the browser and return to the saved search. Review source coverage, title fit and unknown criteria, check jobs of interest, and tap **Add selected jobs to pipeline**. Download the search report when useful. Selecting jobs does not send applications or mark them Applied.

Each workspace uses its own configured Greenhouse, Ashby and Lever boards. Unsupported sources remain visible. Limits are one active run per candidate, two simultaneous board workers per run, ten minutes, 100 boards and 250 saved results. Broader ATS sweeps and AI evaluation are future increments.

Saved reports are in candidate `data/search-reports/`. Receipts, original targeting snapshots and selection checkpoints are private in `.hosted/search/`. Runtime scratch files and caches are excluded from document exports and snapshots. Reports and receipts are backed up. There is no automatic pruning added here.

If selection is interrupted, retry in the same saved search. Canonical writers reconcile pipeline/history without duplicates; backups and exports refuse an unresolved publication rather than record an inconsistent state. Prior pipeline/history bytes are kept in the private publication checkpoint.

## Verification after activation

Confirm both authenticated Search tabs appear, existing editing still saves, and generic worker routes remain blocked. Run the first real candidate searches and review their coverage/quality. Owner phone acceptance and real-candidate selected-offer writes are recorded separately from fictional staging and the public-board probe. The latter uses fictional inputs and proves transport, not candidate eligibility.

## Roll back code

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-search-01/portal/deploy/activate-search.py --rollback
```

Rollback restores the previous editor and backup definitions. It keeps all candidate files, selections and search receipts. Keep both previous releases because restored backup units may still reference them. Never upload Mac backups over VPS edits.

## Later AI increment: required decisions

Before implementing AI evaluations and application drafts, choose the provider/account and verify its VPS access; approve the exact candidate data shared and retention terms; set per-run and aggregate spending limits; and agree on the first generation workflow. An existing Mac subscription is not assumed portable. The server must enforce approved caps before calls. Drafting reuses career-ops evaluation/apply modes and primary candidate facts, with human review and manual submission.
