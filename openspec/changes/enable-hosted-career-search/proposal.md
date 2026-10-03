## Why

Steve and Brad can now view and edit their authoritative VPS files, but cannot search for opportunities from their phones. A browser search and saved shortlist will make the hosted workspace useful for the job hunt without requiring a local coding session.

## What Changes

- Add a candidate-specific Search page with free scans of configured public job boards, saved run summaries, preliminary rankings, and explicit selection into the existing pipeline.
- Reuse career-ops scanners and canonical writers, with durable jobs, bounded resource use, reconnect and cancellation.
- Distinguish confirmed criteria, unknown criteria, source failures, and title-based fit. Preliminary rankings are not the full AI A–F evaluation.
- Preserve the shared login, separate candidate data roots, direct editing, history, and scheduled backups. No candidate files enter Git.
- Deliver Phase 2B in two increments: B1 is free search and shortlist; B2 is AI evaluation and application drafts after a separately reviewed provider, data-sharing and budget decision. This change specifies B1; design records the B2 integration path.
- Do not enable applications, outreach, paid workers, arbitrary commands, or automatic submission.

## Capabilities

### New Capabilities

- `hosted-career-search`: Bounded browser-started public-board searches, durable candidate-specific results, honest preliminary ranking, and selected-offer publication through canonical career-ops writers.

### Modified Capabilities

None. The canonical OpenSpec spec inventory is currently empty; editing and portal changes remain separate in-flight changes.

## Impact

Affected areas include hosted workspace navigation and APIs, scanner adapters, the code-only deployment bundle, job receipts in external candidate roots, and verification of existing Caddy workspace routing. Existing web discovery adapters are reusable, but their streaming lifetime and client-supplied offer publication need adaptation. Existing AI routes assume a complete local checkout and are not enabled by this change.

Current authorization is Phase 2B planning. Implementation and live activation require approval of this concrete B1 proposal; B2 requires additional owner decisions.
