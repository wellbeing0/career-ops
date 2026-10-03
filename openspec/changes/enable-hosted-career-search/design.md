## Context

See proposal.md for motivation and authorization. Production has separate Steve and Brad services and external authoritative data roots. Caddy currently exposes only the hosted editor and static assets; discovery and worker routes remain blocked.

The web discovery adapter already invokes the core scanner, handles JSON/legacy output and reports dataset freshness and caps. Its streaming request is not a durable job. Its title-fit annotation is not a full evaluation. Existing AI worker routes still require mode and script paths under a complete data checkout, whereas hosted code and candidate data are deliberately separate.

## Goals / Non-Goals

**Goals:** Reuse canonical search and publication behavior; survive phone disconnections; give candid counts, uncertainty and source coverage; preserve editing and reliable recovery.

**Non-Goals:** No broad AI route activation, new scoring engine, application submission, continuous monitoring, or unbounded whole-ATS sweep. Shared login continues to allow both people to see both candidates, with server-enforced separation of storage and writes.

## Decisions

### 1. Two increments

B1 delivers free search and shortlist under this change. B2 will have its own concrete specification for AI evaluation and application drafts once provider, identity, retention/data sharing and budgets are decided. Planning both as a single activation would leave paid-worker authority undefined. B1 needs neither model credentials nor transmission of a CV to job boards.

### 2. Reuse core adapters behind a narrow hosted API

Add Search navigation to each hosted workspace and expose only candidate-scoped start/status/results/cancel/select operations. Reuse scanner/provider adapters and canonical pipeline/history writers rather than enabling the existing generic explore/run routes wholesale. Services derive candidate identity and roots from their fixed configuration; requests cannot select directories, commands, scripts or arbitrary client-supplied offers. Select uses server-held run/result IDs.

Keep code resolution distinct from data resolution. Extend the deployment bundle's explicit manifest to include required scanner dependencies, including plugin engine dependencies, and verify execution from the actual code-only layout. Malformed candidate targeting is a visible setup error, not an empty profile or shipped template fallback.

### 3. Start with configured boards and bounded discovery

The default scan previews the candidate's configured public ATS boards, respecting existing dedup and blacklist rules. Use dry-run JSON where supported, then publish only selected results. Qualify whether candidate board coverage warrants a broader discovery option before enabling it. A full dataset sweep is not the default browser action.

Initial operational bounds: one active search per candidate; two across the current two services; ten-minute run deadline; five simultaneous board requests; maximum 250 saved offers per run; cancellation and limits produce a partial receipt. Adapt these conservative defaults only after measured VPS resource qualification. The existing 768 MB service limit must remain effective, including child processes. Where core flags cannot enforce a bound, the wrapper must enforce it or omit that source mode.

### 4. Durable jobs and consistent publication

Store job metadata and result receipts under candidate `.hosted/search/`, with a random job ID, idempotency key, immutable targeting revision, timestamps, progress, source outcomes, limits and terminal state. Server-side execution outlives HTTP polling. A service restart reconciles unfinished receipts as interrupted unless safe resumption is supported. Cancellation targets only the registered owned process group, with process identity checked; stale PIDs are never blindly killed.

Fetch and rank without holding the editor lock. Stage outputs outside canonical files, then take short publication locks in the documented order: hosted edit lock, followed by canonical writer locks. Backups and browser edits cannot race a multi-file publication. Retry after interruption uses the canonical dedup behavior and a publication receipt, preventing duplicated selected-offer side effects. A failed publication retains results and explains what remains unsaved.

Dry runs can still write scanner cache files. Put operational cache in a separately identified runtime area through an adapter if supported; otherwise explicitly exclude the exact cache subtree from document browsing, exports and archival content. Keep compact run receipts and human-readable saved reports in backups. No cache deletion or backup pruning of existing candidate files is included.

### 5. Honest preliminary ranking

Reuse title-fit diagnostics for ordering, alongside explicit facts available from postings. Display verified constraints separately from unknown salary, benefits, work authorization, travel and remote-location restrictions. A title-only match is never labeled as meeting the whole profile or given an A–F score. Unsupported candidates or facts stay unknown. Provide source URL, retrieval time, dedup counts, candidate targeting revision and source freshness.

Show counts for discovered, already known, excluded on explicit evidence, and needs review. Source errors and expired/stale coverage stay visible even when some offers succeed. Optional JD enrichment uses supported public ATS fetching with bounded requests and source capture; unavailable fields are not inferred. A saved report includes ranking reasons and uncertainty so Brad can discuss the shortlist with Steve.

### 6. Keep the trust boundary

Public postings are data. No text from them can start commands, change roots, reveal secrets or authorize writes. Restrict fetches to supported public HTTPS ATS providers, validate destinations and redirects against private/local networks, and reject arbitrary URL targets in B1. Mutations require existing gateway authentication and same-origin checks. Results, receipts and exports exclude credentials and other-candidate files.

### 7. B2 integration path

Later reuse the career-ops evaluation/apply modes, JD archiving, canonical report numbering and tracker writers. First repair split-root assumptions and qualify worker isolation on this VPS. Use primary candidate facts only for draft claims; source-backed figures, employment titles and authorship must survive validation. Drafts and evaluations become downloadable browser artifacts; tracker status never becomes Applied through generation alone.

B2 needs an owner-approved provider/account, exact permitted candidate information, retention policy, per-run and aggregate caps, and an enforced server-side preflight. Availability of a Mac Codex or Claude subscription on the VPS is not established. No credentials or paid calls are necessary to complete B1. These are B2 entry decisions, not unresolved implementation decisions for B1.

## Risks / Trade-offs

- [Free ranking lacks full JD analysis] → Name it preliminary and show unknown criteria; add verified enrichment where supported.
- [Phone disconnect or restart] → Durable receipts and polling; terminal interrupted/partial states rather than false success.
- [Unreachable boards or stale datasets] → Source-by-source coverage and freshness; successful-empty differs from failure.
- [Scanner writes outside the preview contract] → Fixture qualification of cache and canonical side effects before activation.
- [VPS memory pressure] → Conservative concurrency/deadline/caps; test both candidates alongside editing and backups.
- [Candidate changes profile during a scan] → Preserve the run's targeting revision and label it outdated against the new profile.
- [Historical samples contain older job data] → Keep existing documents and link their dates; never silently refresh or overwrite them.

## Migration Plan

1. Implement and qualify locally with fictional candidate roots and provider fixtures. Bundle scanners with an explicit dependency manifest.
2. Stage a versioned release and qualify both candidate base paths with temporary fictional roots, including failure/restart/cancel and backup coexistence.
3. Prepare a reviewed activation helper with exact release, services, backup helper paths and existing Caddy routing. Preserve prior editor/portal releases and backup unit dependencies.
4. With activation authorized, switch code and validate live authenticated routes. Start with read-only navigation/status checks; any real candidate scan or selected-offer publication needs recorded scope.
5. Record staging versus live versus owner mobile acceptance separately. Rollback switches code to the accepted editor release while retaining Caddy authentication and routes, preserving candidate data and receipts; no Mac upload overwrites VPS data.

## Open Questions

Owner may choose which candidate to demonstrate first and the example boards for the live acceptance session. Neither changes the B1 architecture. Provider and budget choices belong to the later B2 proposal.
