# Search review and filter editing

Activate the qualified `20261003-search-review-01` release:

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-search-review-01/portal/deploy/activate-search-review.py
```

Both candidates retain shared login, VPS authority, existing data and backup timers. Exact-address source repairs run as each candidate's service user, taking a filter-history checkpoint. Owner-customized addresses and all search preferences are retained. Lindy and W&B become visible manual sources; Hightouch remains a visible API coverage failure rather than being silently mapped to a historical board.

In either workspace, select Search, then Existing opportunities or View / edit job filters. Save filters directly; previous versions can be restored from the filter editor. Title/location/description lists are editable one keyword per line. Other supported rules have an optional YAML editor. Old results remain dated; a new search uses changed rules. Unknown salary and eligibility still need review. No application is sent.

Rollback code and service definitions:

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-search-review-01/portal/deploy/activate-search-review.py --rollback
```

Rollback does not delete candidate data or reverse owner filter edits/source repairs. The source-repair checkpoint remains available in filter history when reactivating this editor. No Caddy configuration change is required.
