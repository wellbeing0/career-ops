# Interaction feedback and project-aware Assistant release

Release: `20261007-experience-context-01`.

After qualified staging, activate from the VPS as an administrator:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261007-experience-context-01/portal/deploy/activate-experience-context.py
```

This changes only web-code and backup-helper paths for Brad and Steve. It validates source/build hashes and the deployed project-knowledge manifest first, privately journals existing definitions, and restores them on startup failure. Shared login, authoritative candidate files, histories, backup timers, OpenClaw models/settings and the existing provider chain stay intact. Do not run the historical Assistant installer to activate this code-only change.

The knowledge bundle names the wellbeing0 GitHub fork and the upstream project, and explains the actual hosted search, filters, deduplication, preliminary title ranking, Pipeline, Applications, Documents and supported Assistant operations. It comes from the exact deployed code commit; rollback restores the matching documentation. Candidate-specific operational snapshots are read-only and timestamped. No native model tools or arbitrary repo reads are enabled.

After activation, check both workspaces. Buttons should show pointer/press/focus states and busy labels; current navigation should be highlighted. Edit an unsaved profile/CV field and check the notice, then cancel or restore your text. Ask each Assistant which GitHub repo is used, how Search differs from Pipeline and Applications, and how to interpret its latest search counts. Compare answers with the displayed search report. Technical fixture success is not a real-model answer-quality acceptance.

Rollback, if needed:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261007-experience-context-01/portal/deploy/activate-experience-context.py --rollback
```

Rollback changes code paths, not candidate edits or search results. Retain this release while backup definitions reference its helper.
