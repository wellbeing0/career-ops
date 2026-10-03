# Verification and handoff — October 3, 2026

## Completed

- All 874 web tests passed, including four new catalog/isolation/exclusion tests. TypeScript typecheck passed. Python deployment helpers compiled. Git diff whitespace check and strict OpenSpec validation passed.
- Code-only package contains 643 hashed source files. Both candidate production builds completed on the VPS under hosted configuration. Every source hash was checked before and after qualification. Qualification receipt is private at the staged release QUALIFIED file.
- Fictional-root HTTP checks passed for Brad and Steve: gateway authentication, disabled generic workers, document catalog/read routes, traversal refusal, forbidden document writes and foreign origins, saved search results and report downloads. No candidate production writes or provider billing were used.
- Phone-size 390x844 browser checks passed: Documents navigation, archive filter, current search report preview, Steve direct Documents link, no horizontal overflow, pipeline navigation, profile/CV recovery label, filter save/restore, selection, reload, disconnect and cancellation. Zero page errors and zero save dialogs.
- OpenSpec autonomy checker found no supported generated skill copies in this project; no generated OpenSpec skills were altered.

## Owner activation pending

Staged code release: /home/codex-deploy/apps/career-ops-editor/releases/20261003-documents-01
Brad build: gq0wzH5DgaS7wIJuTxvuS
Steve build: CEgZKuyNSWxLiWHJZhcP7

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-documents-01/portal/deploy/activate-documents.py
```

Activation switches qualified code and indexes the currently published historical snapshot by verified hashes under the candidate edit lock. It retains shared login, authoritative documents, search results, history and enabled backup timers. The helper supports --rollback to restore earlier code/service definitions.

After activation, open both workspace Documents tabs, see current search reports alongside dated archives, preview a current text document and download an original. This is the owner/live acceptance step; staged fictional tests do not substitute for it. No commit or push was requested.

## Next AI phase

The next-ai-phase.md plan incorporates Steve’s confirmed VPS OpenClaw provider order: OpenAI subscription first, paid OpenRouter second. Official OpenClaw documentation describes an HTTP agent interface suitable for a server-side Career Ops adapter without a messaging channel plugin. Installed version/configuration, candidate-scoped tool isolation, fallback-spend limits and a capped live trial remain future work. No AI endpoint, personal Telegram setup or provider configuration was changed.

## Navigation/theme follow-up — live verified

Steve confirmed the live Documents tab behaves as expected after sudo activation. Published a static presentation-only release 20261003-live-documents-navigation-01, retaining 20261003-editor-navigation-01 for rollback. All archived original bytes and the snapshot timestamp were preserved and the rebuilt manifest verified before switching the symlink. Seven portal tests passed. Phone-size 390x844 checks passed for home/candidate live links, archive labels, no overflow and both OS light/dark appearances.

Authenticated production probes confirmed both home document links target /{candidate}/workspace?view=documents and archive indexes are labeled. Brad’s live inventory contains 119 current documents, 3 search reports and 46 archive entries; Steve’s contains 60 current documents, 2 search reports and 42 archive entries. Counts are a point-in-time observation. Production CSS includes the device dark-theme palette. No Caddy/auth/service or authoritative candidate-document writes were required.

The separate add-hosted-career-assistant OpenSpec change is now created and strict-validation passed. Its implementation tasks remain pending authorization and runtime/provider decisions.
