## Context

Core career-ops and its optional Next.js alpha web UI share file-based candidate data. The existing web UI includes write and worker endpoints and has no shared-account authentication suitable for this deployment. The inspected VPS runs Caddy, Node 24 and has sufficient available memory/storage. The restricted deployment account can stage applications but cannot change administrator-owned Caddy configuration. No OpenSpec root previously existed in this project.

## Goals / Non-Goals

Goals: a shareable viewing portal with useful document navigation, explicit two-root export, original downloads and reproducible private snapshot releases.

Non-goals: live edits, CLI/provider credentials, AI workers, automated scans, browser application control or exposing the experimental upstream web UI in this release. These capabilities belong to a follow-on change, not a hidden disabled menu.

## Decisions

1. Static export with Python standard library. It serves the required documents without a database or long-running AI/application service. Unlike exposing Next.js behind blocked buttons, it contains no write endpoints at all.
2. Allowlisted document types/areas plus explicit exclusion of migrations, recovery, code, raw receipts and secrets. Include job-search notes because the owner explicitly authorized pertinent files and shared visibility. Raw receipts and repeated source captures add no useful reading experience. Private manifests record selection and omissions outside the webroot.
3. Escape Markdown/text before minimal formatting; suppress JavaScript on document pages, sandbox original HTML previews and block third-party embeds with CSP. Local site code is independent from imported source HTML. Original files remain downloadable behind authentication.
4. Caddy HTTPS basic authentication at the host boundary. One dedicated shared username/password meets the owner-approved access model; its hash resides in a root-owned private Caddy fragment, never in the served directory. Do not reuse credentials from another site automatically.
5. Candidate roots stay on the Mac as source of truth. Private release snapshots reside on the VPS under the deployment account. Staged directories and original downloads are world-readable only as filesystem requirements for Caddy, but never publicly served before authenticated configuration is installed.
6. Immutable release directory, hash verification and atomic `current` symlink replacement. Keep previous releases for explicit rollback. Authentication and Caddy routing persist independently across document updates.

## Risks / Trade-offs

- Shared login grants access to both directories and cannot identify individual edits → authorized by owner; phase 1 cannot edit.
- Snapshot can become stale → prominently show publication and source timestamps; republish deliberately from local sources.
- Historic samples may contain dated facts → preserve dates, draft warnings and original content; publishing is not endorsement of a ready application.
- HTML/PDF originals are active-document formats → restrict inline rendering with CSP and sandbox; download remains an explicit visitor action.
- Full candidate data is larger than the relevant reading set → record omitted paths/reasons; do not silently imply full filesystem mirroring.
- An administrator step is unavailable to deployment account → stage and test everything independently; provide exact sudo installer command and leave live acceptance pending.

## Migration Plan

Build to an external private directory, run selection/render/escape/hash tests and inspect the resulting portal. Stage release plus installer on VPS, verify all hashes and atomically point `current` at it. Owner runs installer using administrator sudo, enters a dedicated login interactively, validates and reloads Caddy. Probe unauthenticated pages/downloads and authenticated navigation, mutation denial and excluded paths. Record evidence and only then mark live deployment accepted. Roll back the document symlink or restore the backed-up site configuration separately.

## Follow-on scope

Phase 2A: one isolated upstream web instance per candidate, shared login wrapper, backups and controlled editing through canonical scripts. Phase 2B: qualify CLI/provider access on VPS, queued work with cancellation, worker capability limits, cost caps and auditable output. Phase 2C: separately qualify remote browser-assisted forms with human submission. No subscription login, keys, spending or provider activation are implied by this phase.
