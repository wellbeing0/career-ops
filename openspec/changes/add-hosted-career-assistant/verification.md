# Verification — October 3, 2026

## Implemented and qualified

The candidate-bound Assistant UI supports continuing conversations, streaming replies, cancellation, safe job context selection, drafts, explicitly selected profile/CV edits, free search and adding a browser-selected saved match through canonical helpers. Drafts appear in Documents. Conversation records and operation results live in private VPS candidate roots, with shared-login attribution. Master CV/profile saves use current revisions and automatic history. Deterministic operation IDs and post-save recovery prevent replay after an uncertain save. The browser retains request identifiers for uncertain initial-request retries.

All 886 web tests and 10 portal/config tests passed. TypeScript typecheck, Python helper compilation, whitespace checks and strict OpenSpec validation passed. OpenSpec autonomy check reported no supported generated skill copies; none were changed. Twelve new assistant tests cover transport restrictions, candidate binding, streaming, drafts, numeric/source safeguards, closed action fields, backups/conflicts, cancellation, credential-error masking, interrupted-save recovery, linked-file denial, profile updates, worker startup grace and temporary lock contention.

Installed OpenClaw 2026.9.3 (1391f7c) was inspected under Steve’s VPS user. Main subscription auth reports healthy in read-only status. Fictional installed-gateway tests passed authentication, both targeted career-agent routes and zero model tools under a permissive global tool profile. Two local fake model calls were made per gateway fixture; no real or paid providers were contacted. The installed schema supports the per-agent disabled memory search/heartbeat policy. The existing personal memory route uses OpenRouter embeddings and is retained globally; career overrides disable it. Native personal subscription credentials are identity-owned and are not copied into new agent stores.

Two hosted production builds completed on the VPS. All 657 packaged source hashes were verified before and after final qualification. The private QUALIFIED receipt records builds, browser checks and backup drills. Brad build L2bbz-vT4sgOID9mK745c; Steve build x1TTebZOd4INqV6X9rwTA.

Phone-size 390x844 browser qualification passed chat, draft saves, reload, cancellation, live Documents visibility and Steve/Brad conversation separation with zero page errors. HTTP checks passed gateway authentication, foreign-origin denial, foreign-candidate conversation denial and same-key retries. A deliberately hostile fake response proposing a CV write in Discuss mode was rejected with the original CV unchanged and a single provider request. Existing search, filter editing, pipeline selection, reload, disconnect, cancellation and document-library regression checks passed. Both candidates’ fictional assistant state was included in verified backup/restore drills.

The adversarial test revealed checkpoint lock contention; worker checkpoints and canonical action execution now retry short 503 lock conflicts for a bounded five seconds. A regression test reproduces this condition. Private per-run logs aid diagnosis without exposing raw logs or credentials to the browser.

## Owner activation complete; live model acceptance pending

Owner activated: /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-02

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-02/portal/deploy/activate-assistant.py
```

Activation pins the inspected OpenClaw version, validates actual staged configuration, journals private before/after files, preserves main/Telegram/personal provider settings, adds bounded career agents and explicit main ambient routing, enables the private HTTP endpoint and switches qualified web builds. All native model tools are denied for career agents. The server fixes agent/thread routing and wraps plain-language requests so native slash commands are not forwarded as operator entry points. Career model fallback preserves the existing OpenRouter list under Steve’s account-level spending control; semantic memory and scheduled heartbeats are disabled. The personal assistant’s original fallback and memory settings remain intact. No model request is made by activation.

Rollback uses the same helper with --rollback, refuses to overwrite subsequently changed config, restores previous runtime/web definitions and retains documents/history/conversations. Credentials stay private in existing server config and root-only service/journal files; they are not in the code package or browser.

Real subscription eligibility for the two newly targeted agents, model grounding quality, actual personal Telegram routing and owner phone usability have not yet been demonstrated. Run a live trial after owner activation using the approved existing provider chain. Steve confirmed his OpenRouter account limit replaces any app-level spending gate. No additional API key or provider chain is authorized. No real-provider calls, paid calls, application submissions, outreach or automatic Applied changes occurred during qualification. No commit or push was requested.

## Credential-reference activation repair

The owner’s first activation stopped before service/config changes because the gateway token is a built-in store SecretRef rather than a literal. Release assistant-02 resolves only the approved store reference through the pinned native resolver as Steve and captures the result in a private root-process pipe. It preserves the original reference. Fictional resolver tests cover correct binding, refusal of exec references and unsafe token values; no actual secret was accessed for diagnostics. Installed-schema validation passed with the real reference retained. Steve approved automatic OpenRouter fallback under his account limit and removed any app-level spending gate. The owner subsequently activated the replacement release successfully.

## Live activation verification

Steve supplied the successful assistant-02 activation output on October 3, 2026. Read-only follow-up confirmed both candidate services active with assistant-02 as their working directory. Authenticated public Assistant endpoints returned enabled=true and the configured OpenAI-first/OpenRouter-fallback status for both candidates. No model request was made by this check. Live provider authentication, response quality and owner acceptance remain pending a first conversation.

## Save response usability update

The owner reported that chat could not save a prior useful reply. The repair adds an explicit Save response button to every completed assistant message, including existing conversation history. It exports the existing text without provider access, returns a current-document download link and persists that link across reload. Saved exports are labeled as AI review material rather than verified candidate facts. Deterministic candidate/conversation/message paths make retries idempotent; modified exports are never overwritten. The server rejects foreign candidate conversations, non-assistant messages and linked output paths. Two regression tests cover these boundaries. The draft operation is now labeled Create a document draft, and the model prompt explains the actual UI save controls.

All 888 web tests, 10 portal tests, typecheck, Python compilation, strict OpenSpec validation and whitespace checks passed. On the VPS, 390x844 browser tests passed response saving, direct download, reload, chat, draft saves, cancellation, candidate separation and zero page errors with a fictional provider. Existing search/filter/pipeline/Documents regression checks passed. Export adds zero model calls; no real provider calls were made. All 658 packaged source hashes were verified. Brad build -geDeVUJpGYlODbcHGJfC; Steve build MYlcXRjIrLBKi8E7RbOoR. The unchanged backup and gateway implementation retains assistant-02 qualification evidence.

Owner activated and accepted: /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-responses-01. The code-only activation helper preserves existing OpenClaw configuration, model chain, credentials and candidate data.

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-responses-01/portal/deploy/activate-assistant-responses.py
```

## Response-saving live acceptance

Steve confirmed the Save response update worked on October 3, 2026. A subsequent read-only service check verified both candidate services active on assistant-responses-01. This establishes owner acceptance of response saving, while broader Brad usability and observed provider routing remain separate checks.

## OpenClaw upgrade review — October 7, 2026

Read-only inspection confirmed OpenClaw 2026.9.8 (fc23bc8), valid configuration and active gateway service. Public /v1/models and /v1/chat/completions remain blocked with 404; the owner portal root returns 200. Career gateway/editor listeners remain loopback-only. Both candidate profile, search, Documents and Assistant APIs respond successfully through authenticated ingress. Both backup timers are active and their latest backup service outcomes are success/exit 0.

Isolated installed-runtime qualification passed gateway authentication, both career agent routes and zero native model tools using two local fictional model requests and no paid providers. The fixture’s original version label was static; the final run labeled the actual installed version correctly. This verifies transport and tool restrictions, not live GPT-6.1 response quality.

The global primary is now openai/gpt-6.1-sol with thinkingDefault high. Both career agent entries still explicitly use openai/gpt-5.6-sol and the existing OpenRouter fallback, with no per-agent thinkingDefault. Brad’s OpenClaw main/console session has a gpt-6.1-sol/medium override; his website-bound sessions still report gpt-5.6-sol. Console session overrides do not set the default for new website conversations. Recommended next change: explicitly set career-brad primary to openai/gpt-6.1-sol and thinkingDefault medium, preserving fallback and restrictions; leave Steve’s selection unchanged unless requested. No configuration was changed during this review.

Career tool denial, disabled semantic memory, zero scheduled heartbeat policy and empty skill/subagent allowlists remain configured. A separate enabled weekly skill-collection-review-career-brad cron job exists and its latest run failed; its error text was classified as tool-related without displaying the raw error. The heartbeat cron entry is disabled. Review the weekly maintenance job separately rather than relaxing career agent tool restrictions.

The original AI activation helper intentionally pins OpenClaw 2026.9.3 and its referenced bundled secret resolver no longer exists in the upgraded installation. Running that original installer on the new version will refuse qualification; current running web workers use their existing private service credential and are operational. Refresh the installation/qualification path before further gateway reinstallation. No model changes, scheduler changes, live AI requests or credential reads for diagnostics were performed.
