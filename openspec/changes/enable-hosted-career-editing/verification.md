# Phase 2A implementation evidence — 2026-10-02

Implementation authorized by Steve's “Proceed” following the reviewed plan and VPS-authority decision. This release is staged; administrator installation and production acceptance are still pending. No live candidate dataset or Caddy routing has been switched.

## Verified

- Hosted profile/CV APIs, minimal navigation, candidate base paths, production proxy allowlist, private gateway requirement, same-origin guard and nonce CSP implemented.
- Profile edits preserve unrelated YAML fields, refuse malformed YAML, require targeting projection review, remove recognized legacy targeting sections, and reject duplicate targeting headings. Original narratives remain recoverable in checkpoints.
- Source-bundle SHA preconditions, exclusive candidate saves, interrupted transaction recovery, dead-owner lock recovery and backup-before-write behavior tested. Recovery guard failures stop safely rather than weakening the lock.
- Existing tracker rows use canonical `set-status.mjs`, with a whole-tracker SHA checked inside its core lock; status ledger and existing notes preserve parity. No new/delete rows are exposed.
- Profile/CV history, preview/restore as new revisions, shared-login audit and credential/runtime-excluding candidate export implemented.
- Full checksum-verified candidate migration copies: Steve 78 files, Brad 130. Repeat migration to an existing dataset refuses to overwrite it. Mac pre-cutover checkpoint retained outside the repo.
- Full Brad scratch migration restore drill passed (131 files including the authority marker). Fictional dataset snapshot/restore drills passed for both Linux runtimes.
- Retention held without acceptance; scratch explicit acceptance plus pruning kept 30 daily / 12 weekly snapshots. Revisions use a 90-day cutoff. Prepared timers do not enable pruning or start before acceptance.
- All 854 web tests and the relevant canonical tracker suite passed; typecheck and both production builds passed. Production dependency audit reported zero vulnerabilities. Local real Chrome test verified hydration/CSP, CV save/reload and blocked automation.
- Linux production qualification ran both candidates concurrently, with disposable gateway/authentication only. Every source API route other than `/api/hosted` was probed with GET/POST and denied. Unauthenticated hosted APIs/writes were denied. Forged candidate/root query fields did not switch roots. Stale CV saves returned 409; canonical tracker write/ledger, export and nonce CSP passed.
- Exact site route structure validated by VPS Caddy 2.6.2. Temporary loopback Caddy authenticated both APIs and denied a worker after authentication. Its admin endpoint was disabled and production Caddy remained untouched.
- Linux restart preserved Steve's scratch saved CV. Last measured process RSS: Brad 134880 kB, Steve 134652 kB (about 132 MiB each); available VPS memory remained about 4.8 GiB after builds.
- Packaging qualification caught a missing system tracker-alias table. Added `tracker-aliases.json` and durable code-only packaging helper; canonical Linux tracker operation then passed.
- Existing career portal still returned HTTPS 401, as expected; the main site returned HTTPS 200 and production Caddy remained active.

## Remaining production gates

Run the administrator installer to create isolated system accounts, checksum-import private datasets, configure loopback services and replace only this site's Caddy routing. Then verify actual authenticated production edits and candidate OS permissions, retain shared login, review the actual targeting projection and confirm owner acceptance. Enable daily backup timers only after this verification. Keep pruning disabled until explicit acceptance/enablement. Code rollback must preserve candidate data; the installer and handoff provide viewing-only rollback.

The change is not archived or declared production-complete. The remaining checks are distinct from staging and fictional-runtime evidence.

## Production installation — 2026-10-02 21:22 UTC

Owner ran the administrator installer. Reported migrations verified Brad 130 files and Steve 78, with successful full restore drills (131/79 files including authority markers). Caddy configuration validated and both services enabled. Follow-up live probes confirmed careerops-brad, careerops-steve and Caddy active; both private roots are mode 0700 and owned by their respective dedicated users. Viewing root, both workspaces and both hosted APIs return HTTPS 401 without credentials. Backup timers remain disabled. An authenticated browser session was not available to the agent; actual logged-in editing and owner review remain pending. VPS is now authoritative; Mac sources are backup copies.

## Authenticated production checks — 2026-10-03

Owner enabled the dedicated testing login; password remains in a mode-0600 private VPS netrc file, outside code and candidate exports. HTTPS API checks passed for both candidates: authenticated read, whitespace-only CV save and reload, stale revision refusal (409), explicit history restore and byte-for-byte equality of every source file with its starting value. Disabled worker POST returned 403. No profile facts or tracker statuses were changed. Both candidates still require owner targeting-projection review before profile saves. This is production API evidence; phone-browser interaction and owner acceptance remain separate pending checks.

## Document-library navigation repair — 2026-10-03

Owner phone screenshot established that the document library lacked a path to editing. Added prominent edit links on home and both candidate catalogs, renamed catalogs as document libraries, and removed stale Mac-authority/phase-one-only wording. Published navigation-only release 20261003-editor-navigation-01 from the current VPS snapshot; every original document byte and snapshot date remained unchanged. All seven portal tests passed; authenticated HTTPS checks confirmed correct editor links on all three pages. Prior release retained for rollback.

## Direct-save update — 2026-10-03

Steve explicitly approved removing the initial targeting gate and ordinary-save dialogs. Profile Save now automatically reconciles recognized targeting sections with structured fields after checkpointing originals. Committed source snapshots are returned under the save lock, so source revisions advance without reloading unrelated drafts. Tracker saves refresh only tracker rows and clear only the saved row’s draft. Restore/reload confirmations remain.

All 854 web tests, typecheck and both updated Linux production builds passed. Real Chrome at 390×844 verified immediately enabled profile Save, zero save dialogs, successful profile/CV saves, and unsaved drafts surviving saves in both directions. Linux fictional-data qualification verified first profile Save without a prior review step, consistent managed targeting, source revision checks, canonical tracker writes, exports, backups, all disabled endpoints, private gateway/authentication and restart preservation.

Automatic approval initially rejected the VPS qualification because it appeared to mutate live profiles. Read-only inspection established temporary fictional datasets, separate test processes and ports; retry was approved. A test-gateway port collision was repaired using an OS-selected loopback port, temporary Caddy storage and a fictional document-library root. Final qualification passed. No live candidate data or production services were changed during this update qualification.

The new release is qualified and awaits the owner’s scoped administrator activation command. Phone/live acceptance follows activation; this is not yet a claim that the live UI was updated.

## Direct-save production activation — 2026-10-03

Owner ran the scoped code-only activation successfully. Live service WorkingDirectory values confirm both candidates use 20261003-direct-save-01, and both services plus Caddy are active. Dedicated-login CV checks passed for both candidates: save/reload, stale-save 409, and byte-exact restore of all source files. Production profile checks submitted existing preferences and narratives without an initial review action, then restored the original source bundles with revision preconditions; both passed. No lasting profile, CV, tracker or authentication changes were made by verification. Phone interaction/owner acceptance and daily backup timer activation remain pending.

## Owner acceptance and daily backups — 2026-10-03

Steve confirmed the direct editing workflow works, then enabled both daily backup timers. Live checks confirmed careerops-brad-backup.timer and careerops-steve-backup.timer active and enabled, with their next runs scheduled. Initial installer snapshots and restore drills already passed; the first scheduled daily run is still pending. Retention pruning remains disabled because timers omit --prune; no private acceptance marker enabling deletion was created. Editing is owner accepted and daily backups are scheduled. Preserve the prior release referenced by backup service ExecStart until those units are explicitly updated.
