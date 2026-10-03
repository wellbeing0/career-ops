# Phase 2A planning review — October 2, 2026

Status: planning complete; implementation not authorized by this planning request. Proposal, design, behavioral delta spec and 16 implementation/qualification tasks are saved. Strict OpenSpec validation passes. Corrected the earlier duplicate `context` key so project context now loads without a warning. No application code, live service, Caddy routing, candidate data or credentials were changed.

## Owner decision

VPS is authoritative; Mac copies are backups. This changes the phase-1 snapshot authority model only when the separately approved cutover is implemented and verified. The current site remains viewing-only.

## Recommended next increment

Reuse the existing web UI for two isolated candidate workspaces under the same host/login. Enable profile and master-CV edits, plus existing tracker statuses and notes. Provide review/preview, conflict protection, private history, restore and export. Disable other APIs server-side.

## Complexity assessment

Moderate rather than a simple hosting switch. Most UI/core behavior exists, but the inspected app lacks candidate tenancy, subpath-aware API URLs, stale-edit protection and an ordinary profile form. Hosting also requires separate interactive CSP/routing from the current static portal. The important new work is isolation and safe authority migration, not writing another career engine. No reliable calendar estimate is claimed before the paired production-build and resource qualification tasks.

Implementation order: hosted scope/paths → safe edits and canonical tracker revisions → recovery/authority migration → staged service tests → administrator rollout and live acceptance. Keep AI workers, scans and browser-assisted applications in later separate changes.

## Remaining phase-1 evidence

Owner confirmed logged-in viewing on October 2, 2026. Public TLS/401 challenges are independently verified. Authenticated mutation/private-path denial passed the temporary Caddy test; those exact production checks remain part of rollout readiness rather than being claimed from the viewing confirmation.
