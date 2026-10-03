## Why

The viewing portal lets two candidates review their job search, but changes still require editing files on the owner's Mac. The owner wants each workspace controllable from the VPS, beginning with profile/CV edits and tracker maintenance, while preserving the same career-ops files and avoiding premature AI worker activation.

## What Changes

- Make the VPS authoritative for both candidate datasets after a verified cutover; retain Mac copies as versioned backups/exports, not upload sources that overwrite live edits.
- Reuse the upstream career-ops web application in a bounded hosted-editing mode with explicit candidate paths and separate server-side candidate roots.
- Enable profile and master-CV review/save, existing-row tracker status updates and notes through canonical core operations.
- Add conflict detection, revisioned private backups, recoverable restores and clear active-candidate labels.
- Retain the owner-approved shared login and document viewing; block scans, agent execution, provider/key settings, ingestion, destructive tracker actions and application automation server-side.
- Keep static snapshots visibly dated; distinguish them from authoritative live profile/CV/tracker views.

## Capabilities

### New Capabilities

- `hosted-career-editing`: authenticated candidate-specific edits, authoritative VPS storage, concurrency protection and recoverable migration.

### Modified Capabilities

None. The accepted phase-1 portal remains operational. Its proposed capability is not yet synced into main specs; this change depends on that portal without rewriting its contract.

## Impact

Future modifications to `web/` routing, capability policy, editors, write adapters, deployment/service configuration and focused tests. Canonical status/notes commands may need revision preconditions within the existing tracker lock. Private data, backups and credentials remain outside Git and public file roots. Two candidate-isolated services reuse a pinned code release; no paid dependency, CLI/model login or provider activation is required for this increment.

This is planning only. No application code, VPS service, Caddy rule, live data authority or user file is changed by creating these artifacts. Phase 2B AI workers and phase 2C browser-assisted applications require separate plans and approval.
