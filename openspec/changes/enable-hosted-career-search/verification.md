# Phase 2B implementation and qualification

## Scope and authority

Steve approved implementation and testing of the free browser-search increment. The implementation is staged in versioned release `20261003-search-01`; Steve ran the administrator activation command; both production services now use that release. No authoritative candidate documents or production tracker/pipeline files were modified during implementation. No paid model calls or application submissions occurred.

## Implemented

- Mobile Search tab for both live workspaces; server-owned candidate roots and result identifiers.
- Core `scan.mjs` dry-run preview receipts with bounded offer details. Hosted subprocesses use reconstructed public Greenhouse/Ashby/Lever entries, exclude provider plugins and inherit no model credentials or execution options.
- Durable receipts and targeting snapshots, idempotent starts, cancellation, interruption reconciliation and enforced time/result/board/concurrency bounds.
- Preliminary title ranking, unknown compensation/benefits/remote eligibility, per-source failures and retrieval timestamps; downloadable Markdown reports.
- Selected-offer writes through canonical pipeline/history writers under hosted serialization. Selection checkpoints retain previous bytes; retries reconcile both an interrupted write and a completed write with an unfinished receipt. No Applied transition.
- Backup/export exclusion of scratch/cache and transient lock recovery files; snapshots refuse unresolved publication. Exports use the root's canonical nested-checkout predicate.
- Code-only packaging, both VPS builds, hash-checked administrator activation and code rollback. Existing Caddy workspace routing is reused; the Next proxy adds only the hosted search endpoint.

## Evidence

- Latest web suite: **864 passed, zero failed**; type checking passed.
- Core suite in isolated Git clone without the personal data marker: **11,157 passed, zero failed, nine warnings**. The initial main-checkout run exposed assumptions about repo-local user data; isolation resolved those failures without changing candidate roots. Its unguarded export walker finding was repaired through the canonical predicate. File-gate tests: **12 passed**. Separate scanner/HTTP regression tests: **16 passed**.
- `portal/deploy/qualify-search.mjs` runs real core scanner code against mocked public-board responses in disposable code/data roots. Verified successful empty versus failed source, configured filters, dedup, two candidate runs, cap of 250, direct edits and checksum-verified backup/restore while searching, canonical selection/retry, cancellation, killed-worker interruption and an accelerated deadline fixture.
- VPS worker-tree measurements in fictional qualification: approximately **223 MiB Brad / 140 MiB Steve** at the recorded peaks. Final temporary web processes: approximately **107 MiB / 134 MiB**. These measured fixture workloads fit below the existing 768 MiB per-service limit; they do not prove every large real board's memory behavior.
- Final VPS HTTP/mobile qualification: both base paths pass gateway authentication, malicious-origin rejection, saved results and report downloads. Generic AI/explore/apply/delete routes remain blocked. At **390 × 844**, selection, reload, browser disconnect and cancellation pass with **zero page errors and zero save dialogs**.
- One real Ashby public-board probe, with fictional targeting and temporary storage: **completed**, 62 postings fetched, 34 title-filtered, 28 preliminary matches. This proves public transport and receipt generation; these are not Brad's or Steve's evaluated opportunities.
- Before activation, authenticated production read-only probes confirmed the existing Caddy workspace paths reached the previous editor's disabled-search response. Post-activation evidence is recorded below.
- Final staged source manifest: **627 code-only files, no mismatches**. Both Linux builds have distinct recorded build IDs. Activation verifies these identities before changing service definitions.
- OpenSpec strict validation and Git whitespace checks pass. Autonomy checker reports no supported project-local OpenSpec skill copies; none were generated or modified.

## Evidence locations

Local logs under `/tmp`: `career-search-web-final.log`, `career-search-core-isolated.log`, `career-search-scanner-tests.log`, `career-search-file-gates.log`. VPS staged release contains `build-brad.log`, `build-steve.log`, `qualification-search.log`, `qualification-worker.json`, `public-probe.log` and `QUALIFIED` after qualification. The source hash manifest contains only code-file paths and digests.

## Remaining acceptance

Task 5.5 remains open for the first agreed real-candidate search/selection and owner phone acceptance. Administrator activation and authenticated live checks are complete. The old editor/portal releases remain available. Mac copies remain backups; no migration or upload over VPS edits is part of activation.

## Live activation verification — October 3, 2026

Steve reported successful administrator activation. Read-only SSH and authenticated HTTPS checks confirm both services run from `20261003-search-01`, both workspace pages and candidate-scoped search endpoints return 200, and generic `/api/run` and `/api/explore` still return 403. Both daily backup timers remain active. Initial saved-search lists were empty for both candidates. No real-candidate search or selected-offer publication was triggered by these checks.

Authenticated live browser checks at 390 × 844 passed for both Brad and Steve: workspace navigation exposed Search, clicking it displayed the visible Start free search button, and neither page produced browser errors. These checks did not start searches or edit candidate data.
