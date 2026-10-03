## 1. Scanner contract and packaging

- [x] 1.1 Define the candidate-configured preview adapter and JSON receipt mapping; verify fixture scans distinguish matches, duplicates, blacklist exclusions, empty boards and failed boards without canonical file changes.
- [x] 1.2 Enforce explicit code/data roots and reject malformed targeting; verify fictional Steve and Brad roots never fall back to the repository or shipped profile.
- [x] 1.3 Extend the deployment dependency manifest for scanner/provider/plugin imports; verify scans execute from a packaged code-only release with external fictional roots.
- [x] 1.4 Identify dry-run cache writes and separate runtime cache from candidate document exports; verify export and backup manifests retain receipts but exclude the exact runtime cache subtree.

## 2. Durable hosted search execution

- [x] 2.1 Implement candidate-specific durable receipts and idempotent start/status/results; verify disconnect/reconnect finds the same run and duplicate starts create no extra worker.
- [x] 2.2 Enforce concurrency, ten-minute deadline and 250-offer cap; verify fixture runs terminate with explicit partial reasons and only one active run per candidate.
- [x] 2.3 Implement owned-process cancellation and restart reconciliation; verify cancelled/interrupted receipts retain results and stale process IDs cannot terminate unrelated work.
- [x] 2.4 Restrict public provider destinations and redirects; verify private/local destinations are rejected and posting instructions cannot influence execution.

## 3. Mobile search and saved shortlist

- [x] 3.1 Add Search navigation and candidate-scoped polling views; verify both base paths at phone width expose start, status, results and cancellation without hidden controls.
- [x] 3.2 Reuse title-fit signals with explicit unknown criteria and source freshness; verify omitted salary never counts as verified above minimum and no preliminary rank is labeled an A–F score.
- [x] 3.3 Save a human-readable run report with source outcomes, counts and targeting revision; verify results remain available after reload and profile changes mark older targeting.
- [x] 3.4 Add selection by server-held run/result IDs; verify fabricated payloads and cross-candidate IDs are rejected.

## 4. Canonical publication and recovery

- [x] 4.1 Publish selected offers through canonical pipeline/history writers with receipts and dedup reconciliation; verify retries after injected interruption create no duplicate effects or Applied status.
- [x] 4.2 Integrate publication with edit/backup locking without holding locks during network work; verify simultaneous editing, publication and snapshot restore produce coherent files and history.
- [x] 4.3 Preserve candidate document browsing and existing saved samples; verify new search navigation does not overwrite historical reports or introduce credentials into downloads.

## 5. Qualification and handoff

- [x] 5.1 Run appropriate core/web tests, type checking and both candidate builds; record commands and outcomes and repair failures before staging.
- [x] 5.2 Stage a versioned release and test both fictional candidate roots through the narrow hosted allowlist and verify existing Caddy workspace routing; verify generic AI routes remain blocked and authentication/same-origin checks still work.
- [x] 5.3 Qualify bounded concurrent searches alongside editing and backups on VPS resources; record peak memory, cancellation behavior and restore evidence before recommending activation.
- [x] 5.4 Prepare the exact activation and rollback helper and handoff; verify previous editor/portal releases and existing backup service dependencies remain recoverable.
- [ ] 5.5 After authorized activation, verify live authenticated navigation/status, run the agreed real-candidate acceptance search and selection, and record owner phone acceptance separately from staging evidence.
- [x] 5.6 Prepare the later B2 decision brief using measured B1 findings; deliver provider/account, data-sharing/retention and budget questions without enabling paid calls or application submission.
