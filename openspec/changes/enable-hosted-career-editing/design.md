## Context

Phase 1 serves static document snapshots behind Caddy basic authentication. The owner confirms successful logged-in viewing. Remaining phase-1 live API/mutation/private-path acceptance is not independently evidenced, so it must be closed during the next rollout readiness check, not assumed from that confirmation.

The owner selected VPS authority on October 2, 2026: Mac copies become backups. The existing shared-login access model permits both people to see both candidates and does not authenticate individual identity.

Inspected implementation:

- `web/README.md`: opt-in alpha UI and external `CAREER_OPS_ROOT`/`CAREER_OPS_CODE_ROOT` support.
- `web/src/lib/career-ops.ts`: one process-level data root; no native per-request candidate tenancy.
- `web/src/proxy.ts` and `origin-guard.mjs`: same-origin/host guard, but not authentication or a feature allowlist.
- `api/cv`: GET/POST and prior-content backup; GET currently treats all read errors as missing, and POST has no revision precondition.
- `api/profile`: deep-merge mapping guard but supports a limited patch; `compMin` and `compMax` currently write a target range, not the separate canonical minimum. It deliberately leaves personalization untouched.
- `components/config-form.tsx`: provider/CLI settings, not the profile editor needed here; profile saves currently appear in the assistant console.
- `api/status`: invokes `set-status.mjs`, correctly reusing its lock and ledger. The core supports notes, but neither the inspected HTTP route nor core offers the needed revision precondition.
- `core/safe-write.ts`: crash-safe rename and pre-write backups, not protection from stale concurrent read/modify/write.
- `next.config.mjs`: no basePath; many components fetch root-relative `/api/...`. Subpath hosting therefore needs explicit URL changes and tests, not only reverse-proxy rewriting.

## Goals / Non-Goals

Goals: usable live profile/CV editing and existing-row status/notes maintenance; candidate isolation; VPS authority; recovery; stable document sharing.

Non-goals: new/deleted tracker rows, automatic scoring, tailored generation, scans, job ingestion, file uploads, arbitrary YAML/code editors, provider/key settings, CLI authentication, AI assistant, browser control, email or submission. They are not implied by installing upstream code.

## Decisions

### 1. Reuse the upstream UI with a hosted-editing capability mode

Keep one pinned core/web source release and add a narrowly scoped deployment mode. A server allowlist enumerates enabled pages, GET endpoints and write operations; all other routes fail closed. Hide unsupported navigation as a usability measure, but rely on server refusal. Build a straightforward profile form rather than requiring the AI assistant to save preferences. Reuse the existing CV editor and tracker views with conflict/error handling.

Alternative: build a second custom editor into the static portal. Rejected as the primary plan because the owner wants the new career-ops interface and its canonical behavior; maintain a small hosted adaptation rather than a parallel engine.

### 2. Two candidate-isolated processes, one shared login

Use separate service accounts and private mutable data roots, with a read-only shared code release. Each instance has a fixed data root and cannot traverse the other candidate's directory. Bind both application ports to loopback. Route `/brad/workspace/` and `/steve/workspace/` through the existing hostname/login. Do not use an active-candidate cookie: two tabs must remain independent.

Build with explicit candidate base paths and separate output directories. Centralize client API/download URLs so every enabled fetch stays below the base path. Verify links, assets, redirects and errors in both builds. Cookies/state keys must be candidate-scoped. Preserve `/brad/` and `/steve/` as document landing pages with links to the live workspace.

Caddy will need scoped routes: its current blanket non-GET denial and `script-src 'none'` must continue protecting static content but cannot apply to the interactive Next.js routes. Keep shared authentication before both route classes and retain same-origin protection in the applications. Qualify a production CSP suitable for Next hydration on interactive routes; no external-origin wildcard or dev-only permissive policy.

Alternative subdomains would avoid many base-path changes but may repeatedly prompt for browser basic authentication and depart from the requested single-host directory layout. Avoid a new custom multi-tenant engine in this increment.

### 3. Files remain canonical; VPS becomes the only live writer

Copy the complete private candidate datasets to mutable roots outside static releases, including relevant data/config/personalization, PDFs and source documents. Use a versioned migration manifest to verify files. The first copy is explicit migration, not a repeatable overwriting deployment step. Mark the Mac directories as backups in their procedural `_custom.md` guidance and preserve an original pre-cutover checkpoint. Future Mac work reads/downloads authoritative data or invokes approved remote core workflows; it must not edit backup copies as a second source of truth.

Code, user data, document snapshots and credentials have separate directories and lifecycles. No cloud database is introduced. Static document refreshes use a consistent VPS snapshot, never the retired Mac authority. Live profile/CV/tracker links show current revisions immediately; existing dated application/evaluation files remain immutable historical evidence.

### 4. Profile coherence is part of the edit, not deferred to AI

Structured fields: contact identity, primary roles, base minimum/target/currency, location/travel and US work authorization/citizenship. Preserve unrelated profile keys. Provide explicit Markdown narrative editing for `modes/_profile.md`, not arbitrary filenames.

During migration, preview existing duplicate targeting statements and convert only their target-role, compensation and location-policy sections into a deterministic managed block projected from structured fields, with source provenance preserved. Treat the original text as a private recoverable revision. Unmanaged archetypes, evidence boundaries and narrative stay intact. Per Steve’s approved revision, the first ordinary Save performs this synchronization automatically with a recoverable checkpoint; there is no initial review gate. Never resolve contradictory factual claims through inference. Show unsynced narrative conflicts rather than quietly allowing old compensation/location targeting to override new settings.

A profile save uses candidate-local locking, revision preconditions, backup-before-write and a private transaction intent for the two files. On interruption, recover consistently before further writes. CV facts do not automatically change when a contact/targeting preference changes; the interface points out which source needs explicit review.

### 5. Concurrency and canonical tracker updates

Profile/CV reads return an opaque content revision; writes supply it and compare it inside a candidate-local file lock. Atomic rename alone is insufficient. Invalid/malformed existing content is an error, not absent onboarding data.

Extend the canonical `set-status.mjs` seam with an expected-row revision/identity precondition checked while its existing tracker lock is held; preserve legacy CLI behavior when the precondition is omitted. Use the same core operation for status and notes. Do not add a separate web tracker writer or hold an outer lock that deadlocks the core's lock. Add focused parity and concurrency tests with fictional datasets. Show conflicts and retain unsaved browser text. No default Applied transition follows draft creation.

### 6. Private revisions, exports and backups

Retain individual successful-write revisions for 90 days and full daily snapshots for 30 days plus weekly snapshots for 12 weeks, with private owner-only storage. Pruning must wait until at least one backup/restore test and recorded acceptance; no cleanup during initial migration. Keep a downloadable candidate export that excludes credentials, locks and runtime caches. Mac copies can be refreshed from this export without becoming authoritative.

Every save records candidate, timestamp, shared principal, operation and before/after revision. An optional visitor-entered label is convenience metadata, never verified identity. Do not log CV text, passwords or model credentials. Restore has preview and confirmation, applies as a new revision and preserves history. A failed backup prevents the write.

### 7. Service and release operations

Administrator setup creates candidate accounts, protected data/revision directories, loopback systemd services and the reviewed Caddy routes. Existing shared credentials stay in their current root-owned fragment. The deployment account manages code releases but does not get general write access to both live datasets. Use an explicit restricted migration/export helper where owner operations require privilege. Routine upgrades switch code releases and restart services without rsyncing candidate data.

## Risks / Trade-offs

- Alpha UI has substantial hidden worker/browser surfaces → explicit server allowlist, no installed provider credentials and direct-request tests for every disabled endpoint family.
- Root-relative fetches and framework scripts complicate subpath hosting → two-build production smoke tests before administrator rollout.
- Two Node instances share a VPS with existing products → measure production idle/peak memory and startup; if headroom is insufficient, retain viewing mode and revisit hosting rather than weakening isolation.
- Profile facts appear in multiple user files → narrowly reviewed migration to a deterministic targeting block; preserve originals and refuse conflicts.
- Shared login cannot identify who made a change → honest shared-principal audit; separate accounts remain a future owner choice.
- VPS-authoritative data needs actual recovery evidence → private backups, export and restore drill on scratch copies before cutover.
- Restoring old code or data can undo current work → separate code rollback from explicit revision restore; never re-import the initial Mac snapshot automatically.

## Migration Plan

1. Run implementation tests against fictional scratch datasets, with no live data or credential changes.
2. Produce two production builds and validate allowed capabilities, CSP, base paths, two-tab behavior and resource use on staged VPS services.
3. Take/hash pre-cutover Mac and VPS checkpoints; copy complete datasets into protected candidate roots. Review personalization projection and inspect conflict findings.
4. Verify file counts/hashes, canonical doctor/tracker checks and restore drills. Define the authority marker; freeze Mac editing before enabling browser writes.
5. Owner authorizes/runs the scoped administrator setup. Enable only the editing routes behind the retained login; keep the static portal available throughout.
6. Verify actual HTTPS/login, authenticated edits, conflict handling, candidate separation, disabled worker paths, ledger entries and code rollback preserving saved changes.
7. Record acceptance. Only then activate the backup schedule/retention and update the local procedural guidance/export labels.

## Later increments

Phase 2B: free ATS scans first, then model/CLI qualification, provider credentials, spend caps, queue/cancel/retry and auditable report/CV generation. Phase 2C: browser-assisted applications with session isolation and explicit human submission. These deserve separate changes and do not block this editing increment.

## Open Questions

No blocking product decisions remain for this plan. Actual production build resource consumption, exact framework CSP and deployment helper privilege shape are implementation qualification tasks with explicit fail/rollback criteria; they do not authorize expanding this capability's scope.

## Implementation decisions (2026-10-02)

Steve approved implementation with “Proceed” after choosing VPS authority. The tracker precondition uses the complete tracker SHA inside the canonical lock, a stronger conflict check than a row-only revision. This rejects unrelated-row changes and avoids stale row identity. Production builds use Next's supported webpack compiler because the local Turbopack build stalled; hosted restrictions are production proxy policy, not development-only behavior. Runtime builds are qualified on Linux before administrator routing changes.

## Direct-save revision approved 2026-10-03

Remove initial targeting review and ordinary-save confirmation prompts. Preserve backup, restoration, validation and revision checks. Profile/CV saves return their committed source snapshot from inside the write transaction; the client advances the saved bundle revision without reloading unrelated drafts. Tracker saves refresh only tracker data and clear only the saved row draft. Restore and explicit discard retain confirmation.
