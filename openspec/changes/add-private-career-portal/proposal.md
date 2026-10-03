## Why

The owner needs to share existing candidate profiles, job-search evidence and application samples with a family member without exposing them publicly. A private viewing portal provides immediate value while keeping the experimental interactive career-ops web application behind a separate future qualification step.

## What Changes

- Build a static, authenticated document portal with two explicitly selected candidate directories and a common shared login.
- Publish job-process documents with rendered Markdown, original downloads, timestamps and clear draft/stale-source notes; exclude credentials, program code, raw fetch receipts, runtime caches and recovery archives.
- Keep local candidate files authoritative; publish immutable snapshots with manifests, atomic activation and rollback.
- Stage the release on the existing VPS and provide an administrator-run installer for permanent Caddy routing, TLS and authentication.
- Document subsequent editing and AI worker migration without exposing those capabilities in phase 1.

## Capabilities

### New Capabilities

- `private-career-portal`: authenticated, read-only candidate document sharing and recoverable snapshot deployment.

### Modified Capabilities

None. Core career-ops file contracts and existing web application remain unchanged.

## Impact

New standalone portal builder, focused tests, deploy scripts and OpenSpec artifacts. Uses the existing Python standard library and Caddy; no provider calls or new paid services. Private documents and credentials remain outside Git. Existing VPS sites and their login configurations must remain intact. Owner authorized implementation and staging; administrator Caddy setup and live acceptance remain separately evidenced.
