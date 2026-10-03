## 1. Hosted scope and paths
- [x] 1.1 Add hosted-editing server capability policy and minimal navigation; verify direct calls to all disabled worker, scan, ingestion, provider, browser and delete endpoints fail without side effects.
- [x] 1.2 Add explicit per-build base paths and centralized enabled client URLs; verify both production builds keep links, assets, requests, state and redirects in their candidate workspace.
- [ ] 1.3 Define fixed candidate runtime roots and least-privilege service layout; verify two-tab edits and forged path/header/cookie requests cannot access the other candidate's data.

## 2. Safe editors
- [x] 2.1 Implement ordinary profile editing with canonical base minimum/target and field-preserving validation; test malformed YAML refusal, provenance retention and no template resets.
- [x] 2.2 Implement reviewed targeting projection/personalization editing and recoverable multi-file saves; test conflicting legacy text, interruption recovery and preserved unrelated narrative.
- [x] 2.3 Add CV revisions, locked save preconditions, backup failures and useful conflict UI; test concurrent stale saves and unsaved-text retention against scratch datasets.
- [x] 2.4 Extend canonical tracker operations with revision/identity preconditions and expose existing-row status/notes; test within-lock conflicts, parity, row identity and standard transition ledger with no duplicate web writer.

## 3. Recovery and authoritative storage
- [x] 3.1 Implement private revision audit, preview/restore and candidate exports; verify restores create new revisions and shared login is not falsely attributed to individuals.
- [x] 3.2 Prepare daily/weekly private backups and retention policy; run a full scratch restore drill and keep pruning disabled before owner acceptance.
- [x] 3.3 Prepare checksum-verified one-time authority migration and Mac backup markers; verify code deployment and repeat snapshot publishing cannot overwrite live datasets.
- [x] 3.4 Mark dated samples/evaluations as historical and live profile/CV/tracker as current; verify post-edit navigation does not imply older documents were regenerated.

## 4. Deployment qualification
- [x] 4.1 Run relevant core/web tests, typecheck and both production builds; verify no developer-only policy is required for hosted behavior.
- [x] 4.2 Stage isolated VPS services with fictional data and measure resource use; verify existing products remain healthy and both candidate processes can be restarted safely.
- [x] 4.3 Prepare scoped administrator/systemd/Caddy changes, production CSP and rollback instructions; verify shared authentication covers all APIs/downloads and no application port is externally exposed.
- [ ] 4.4 After separate implementation/release authorization, checkpoint actual datasets, review profile projection and complete authority cutover; verify hashes, doctor/tracker checks and existing portal availability.
- [ ] 4.5 Verify live saves, conflicts, isolated roots, disabled capabilities, backups/export and code rollback preserving edits; record owner acceptance before enabling retention pruning or archiving.

## Administrator/owner handoff

1.3 remains open for actual system-account permission verification. 4.4 and 4.5 require administrator installation and authenticated production/owner acceptance. Staging evidence is in verification.md; the executable administrator command and rollback are in portal/deploy/PHASE2-HANDOFF.md. No additional product decision is needed to run the prepared cutover.
