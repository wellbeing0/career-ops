# Add hosted career assistant

## Why

Brad needs conversational help with his accomplishments, profile, CV, job comparisons and application drafts without Steve’s Codex desktop. Steve prefers a browser interface and already operates OpenClaw on the VPS with OpenAI subscription access first and paid OpenRouter fallback second.

## What Changes

- Add a mobile Assistant tab inside each Career Ops workspace, continuing candidate-specific conversations.
- Connect through a private server-side adapter to a dedicated OpenClaw career agent boundary, reusing the existing verified provider order.
- Give the assistant bounded career tools for approved primary-source reading, existing search/pipeline operations, draft creation and explicitly requested profile/CV edits.
- Save through current authority, conflict and history mechanisms; display saved outputs immediately in Documents.
- Show model/fallback status, use the existing OpenRouter account spending limit without an app-level spending gate, support cancellation and recover interrupted conversations.
- Preserve the shared login initially with honest shared-login attribution. Named accounts and Telegram entry points are optional later extensions.

## Impact

The hosted web app gains a server-side AI adapter, conversation records and bounded tool integration. Candidate facts and runtime conversations stay in VPS candidate roots, outside Git. Credentials remain private server data. The existing personal Telegram assistant and broad personal tools remain outside this career boundary.

This change is a planning artifact requested by Steve. It does not authorize activating AI endpoints, changing OpenClaw configuration, billing provider calls or sending messages/applications. Installed-runtime inspection and capability qualification precede implementation and release.
