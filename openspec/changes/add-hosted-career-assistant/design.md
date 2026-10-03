# Design

## Decisions

The preferred entry point is Career Ops Assistant, not a new messaging channel. A browser request goes through the authenticated Career Ops server to a private OpenClaw gateway agent run. The server chooses candidate, agent and conversation identifiers; client input cannot choose arbitrary agents, models, scopes or session keys. Separate Brad and Steve conversations survive reconnects. Shared login is currently approved, so audit records identify shared-login and selected candidate, never claim authenticated individual identity. Named logins can be added later if wanted.

Official [HTTP API documentation](https://docs.openclaw.ai/gateway/openai-http-api) describes POST /v1/chat/completions, disabled by default, with model=openclaw/<agentId>, stable user values per conversation and streaming responses. These are agent runs through normal gateway configuration, so the selected agent should use its configured provider chain without a web-side override. Inspect the installed version first; current online documentation is not evidence that Steve’s installed runtime supports these settings.

No Telegram-style channel plugin is needed solely to exchange browser chat. Document operations require separate bounded career tools: a restricted tool plugin or adapter may be necessary depending on the installed OpenClaw extension interface. HTTP chat by itself does not give safe candidate-file editing. Prefer reusing Career Ops core helpers rather than giving the model a shell or unrestricted filesystem.

Steve confirms VPS OpenClaw uses his OpenAI subscription first and paid OpenRouter second. Verify agent configuration inheritance without printing credentials, and preserve that order. Display the configured fallback chain. Steve approved automatic OpenRouter fallback under his existing account limit; no app-level spending limit or accounting gate is required. Verify that each career agent inherits the intended chain.

## Runtime and tool boundary

OpenClaw bearer access is owner/operator authority according to the HTTP documentation. Keep it on private ingress and in server credentials; x-openclaw-scopes does not narrow a shared-secret bearer. Brad must never receive that token. A dedicated career gateway/service boundary is preferred if the existing personal runtime exposes broad tools. A separately bounded agent in that runtime is acceptable only if installed-version tests prove the required limits. Separate agent names and workspaces alone are not operating-system isolation. [Multi-agent routing](https://docs.openclaw.ai/concepts/multi-agent) and [security documentation](https://docs.openclaw.ai/gateway/security) inform this decision.

Expose a small closed tool set, validated outside the model:

- Read approved candidate primary files and relevant job/report data. Treat postings and generated files as untrusted reference data, not instructions or factual authority.
- Start/cancel bounded free searches, inspect reports and add explicitly selected jobs through existing canonical helpers.
- Create clearly labeled drafts under output/ and list them in Documents.
- Apply explicitly requested profile/CV edits using existing revision checks and automatic prior-version history; reject stale edits while retaining the draft.

No arbitrary path, shell execution, gateway administration, personal Telegram, secret access, cross-candidate session lookup, external messaging, application submission or automatic Applied status is exposed. A candidate selection binds the whole conversation and its tools; switching candidate starts or selects a different conversation.

## Conversation and content behavior

The assistant asks for missing experience facts, traces claims to primary sources and never invents accomplishments, authorship or numbers. New factual additions are proposed with source provenance and require explicit candidate confirmation. Routine edits explicitly requested within established authority save without a redundant approval dialog. CV/application outputs are drafts for human review; no submission occurs.

Persist conversation messages, run IDs, candidate binding and operation status in private .hosted storage; recover pending changes using existing transaction mechanisms. Tool calls use operation IDs to avoid duplicate saves after a disconnected stream. Cancellation stops additional model/tool work where supported, reports the confirmed final state and preserves completed files. An uncertain save is resolved from the operation ledger before retrying, not replayed blindly.

Use the existing workspace design and device light/dark preference. Mobile users see streaming replies, saved-file links, missing-fact questions, provider/fallback state and clear retry/cancel actions. Raw gateway errors, tokens and prompt internals are not displayed. A completed output links directly into live Documents.

## Open decisions and inspection evidence

Before implementation, establish the installed OpenClaw version, owner/service location, available private transport and supported restricted-tool mechanism. The deployment account previously saw no executable/system unit in its own inventory; that does not contradict Steve’s confirmed VPS installation. Inspect the actual owner runtime rather than upgrading blindly.

Steve approved the existing OpenAI-first/OpenRouter-second chain, with automatic fallback controlled by his OpenRouter account limit and no application spending gate. Use only the selected candidate’s approved career context. Browser-only is the first scope; Brad’s Telegram ID and bot/account routing are unnecessary unless Telegram is later selected. Preserve the existing personal bot.

## Delivery and rollback

1. Inspect the owner runtime and record version/capabilities and the credential reference locations, never credential values.
2. Qualify a fake/non-billing adapter with fictional candidates and enforced tools.
3. Stage the browser UI and candidate-scoped conversation/tool integration.
4. After activation, run a live trial using the approved provider chain with approved data and verify provider order, grounding, isolation, saves, conflicts, cancellations and document visibility.
5. Supply an owner activation/rollback that can disable AI while retaining existing search/editing/documents and conversation backups.
6. Complete Steve/Brad usability acceptance separately from build/test evidence.

Rollback disables the AI surface/adapter and career-specific runtime configuration, preserving candidate documents/history and existing personal OpenClaw use.

## Installed-version decision — October 3

OpenClaw 2026.9.3 (1391f7c) is running under Steve on loopback port 18789. Actual agent configuration uses agents.entries with a sole main agent. Primary is openai/gpt-5.6-sol; personal fallback is openrouter/~google/gemini-flash-latest. Read-only model status reports OpenAI OAuth healthy. Chat Completions is currently disabled.

The installed runtime treats the subscription account as personal identity-owned model credentials; copying it into new agent stores is expressly unsupported by its native portability schema. Prefer two explicitly targeted career agents in the existing gateway, each with its own fresh workspace/session history and tools.deny=["*"]. The authenticated web server selects those agents and feeds approved candidate sources. The application executes a closed action protocol, not OpenClaw shell/filesystem tools. User messages are wrapped as career requests rather than forwarded as slash-command entry points. Gateway operator credentials stay private on the VPS.

Introducing multiple agents requires explicit preservation of the formerly implicit main owner: Telegram channel-wide binding, heartbeat/system owner and Talk owner remain main. The activation must back up configuration, preserve the main agent, channels and personal model chain byte-equivalently at those fields, validate the installed schema and supply rollback. This is a version-specific choice allowed by the bounded-agent option; an isolated gateway remains an alternative if its subscription-auth sharing is later supported.

Career agents preserve the existing OpenAI primary and OpenRouter fallback list. Steve explicitly relies on his OpenRouter account limit; the app adds no spending gate or accounting. Semantic memory remains disabled to avoid a separate paid embedding route. The existing personal assistant’s configuration is unchanged. The app uses explicit operation choices to authorize supported saves, draft creation, free search and adding only a browser-selected job. Conversational chat is read-only; selecting an edit operation is part of the explicit edit request, not a second confirmation after it. Numeric claims absent from primary sources or direct candidate statements fail the save check. Model grounding still requires live-quality qualification; a numeric guard alone cannot prove every factual sentence.

The current global memory-search embedding route is OpenRouter (openai-compatible, openai/text-embedding-3-small). Career agents override memory.search.enabled=false and rememberAcrossConversations=false, and heartbeat.every=0m; utilityModel is empty to skip an alternate utility route. These per-agent fields were checked in the installed schema. Candidate conversations persist in the app independently of semantic memory. The personal embedding and heartbeat settings remain intact.
