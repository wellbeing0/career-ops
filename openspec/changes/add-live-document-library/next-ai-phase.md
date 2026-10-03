# Next phase: conversational career assistance

## Recommendation

Give Brad an Assistant tab in Career Ops first, so his phone browser is sufficient. OpenClaw can run the conversations and tools on the VPS behind that interface; Telegram can be an optional second entry point. A separate career assistant with explicit candidate workspaces and tools is preferable to extending Steve's general personal assistant with unrestricted access. Reuse the current save/history mechanisms and document inventory: generated drafts should land under the candidate's output area and immediately appear in Documents.

Steve confirms that OpenClaw already runs on the VPS, using his OpenAI subscription first and paid OpenRouter second. Reuse that existing provider order rather than introducing a separate paid API path; the installed runtime and configured agent inheritance still need verification. This is a proposed design, not enabled functionality. The deployment account could not find an OpenClaw executable or system service in its own accessible inventory. This does not prove OpenClaw is absent: the existing Telegram assistant may run under Steve's user or another runtime. Inspect its installed version and actual configuration within that ownership before selecting supported settings. Do not upgrade or reconfigure it merely to match current documentation.

## Supported directions and their limits

[Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent) supports independent agents, workspaces and deterministic channel bindings. A Brad Telegram sender can be explicitly allowlisted and routed to Brad's career agent, with separate conversation/session keys. Adding an allowed sender alone must not accidentally route Brad into Steve's personal assistant. A dedicated career bot/account is an option; preserve the existing personal bot.

The [HTTP chat endpoint](https://docs.openclaw.ai/gateway/openai-http-api) can serve a custom browser interface, with bearer authentication kept on the server and stable application conversation identifiers. Browser chat must use server-selected candidate/agent/session values; a browser-supplied model or arbitrary OpenClaw session key must not grant broader capabilities. The documented endpoint is POST /v1/chat/completions, disabled by default. The server selects an agent with model=openclaw/<agentId> and supplies a stable user identifier per candidate conversation. Calls run through the existing agent runtime, so its normal provider configuration applies unless explicitly overridden. No Telegram-style channel plugin is needed for this browser client. Verify the endpoint behavior on the installed version before enabling it. Shared-secret bearer access carries owner/operator authority; do not expose it to browsers or assume an x-openclaw-scopes header narrows that credential. A scoped career gateway/tools boundary is required.

[Telegram configuration](https://docs.openclaw.ai/channels/telegram) provides sender allowlists/pairing and account routing. Brad's Telegram user ID/account choice is needed only if Telegram onboarding is selected. Browser use does not require him to access Codex desktop or install a CLI.

OpenClaw's [security model](https://docs.openclaw.ai/gateway/security) requires deliberate trust boundaries. Separate agents and sessions do not by themselves enforce operating-system file isolation. Explicitly restrict cross-agent/session tools and use a dedicated career gateway/service boundary if the existing personal assistant has broad capabilities. This is an implementation choice to qualify, not a reason to expose the general gateway to Brad.

## Proposed user experience

1. Open Brad's workspace and Assistant; choose a continuing conversation.
2. Ask for help with accomplishments, profile edits, job comparison, a tailored resume or application draft.
3. The assistant asks for missing facts and cites the candidate's approved primary files. New accomplishment claims need the candidate's confirmation; no invented metrics or authorship.
4. Explicitly requested supported edits save through current revision/conflict checks with automatic previous-version backup. Do not add a redundant approval dialog for routine authorized edits. Generated application material is clearly a draft; applications and outreach are never automatically sent.
5. Saved documents immediately appear in Documents. Conversation state is candidate-bound, survives disconnection and supports cancellation.

Shared login remains approved for document viewing. For AI, separate named logins are recommended for attribution; if shared login is retained, label identity as shared-login and bind a selected candidate workspace without pretending it proves who is speaking. Telegram routing must use verified sender IDs rather than names.

## Decisions required before paid/provider activation

- Browser-only first or browser plus Telegram; whether Brad wants a named login or retains shared-login attribution.
- Exact OpenClaw runtime/owner/installed version and dedicated career service versus bounded agents in the existing trusted gateway.
- Verify the existing VPS OpenAI subscription-first/OpenRouter-second chain, exact model selection and whether Brad’s dedicated agent inherits that configuration. Agree on OpenRouter fallback limits and data-sharing/retention for profile/CV text. Steve’s existing VPS subscription setup is user-confirmed; do not treat that as verification of its installed settings or unlimited fallback-spend approval.
- Which operations may save directly under explicit user instructions and which must remain draft-only. Existing no-submission boundary remains controlling.

## Implementation/acceptance sequence

Inspect the current owner runtime without printing credentials; create an OpenSpec change for the chosen AI design. Build a server-side adapter exposing only candidate read, bounded search, draft generation and validated saves. Qualify with fictional candidate roots and a non-billing fake provider first. Then perform a separately approved capped live provider trial, testing factual grounding, Steve/Brad conversation isolation, cancellation, conflict handling, backups and immediate document visibility. Brad's owner intro session is the final usability check. No provider calls, new accounts, Telegram messages or general assistant configuration changes are authorized by this document-library release.
