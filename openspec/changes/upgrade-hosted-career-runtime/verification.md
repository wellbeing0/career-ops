## Scope and authorization
Steve approved the October 7 upgrade recommendations. This repair targets Brad’s website defaults and deployment helpers. Candidate facts, Steve’s model, personal routing, credentials, shared login and public API restrictions are preserved. No application submission or outreach is authorized.

## Helper verification
Fifteen Python deployment regression tests pass. Strict OpenSpec validation passes. The installed 2026.9.8 native resolver module exports the expected resolver; the interface check does not resolve or display a credential. Unknown versions are refused. Future activation receipts can pin a qualified runtime version; historical receipts retain their original version pin.

The expanded browser qualification passed at a 390 × 844 mobile viewport against the existing production code in an isolated fictional workspace: chat, draft save, explicit response save/download, profile save with previous-version history, reload, cancellation, live documents and candidate isolation. Five local mock-provider calls; zero paid calls; zero browser errors. The fixture adds a fictional candidate name because real profile saves correctly require one.

## Runtime recovery and unresolved monitor
The initial upgrade attempts safely restored prior settings after native cron refused to disable the system-owned review monitor. A subsequent attempt rolled back because the gateway’s startup exceeded the old 30-second window. Installed logs showed normal startup taking approximately 65 seconds; the repair now allows a bounded 180-second startup window and does not restart on a failure before configuration mutation.

OpenClaw’s installed `skill-collection-review-monitor` implementation enables these monitors from the global Skill Workshop autonomous mode. Native `cron disable` rejects system-owned jobs. Disabling that global setting would affect other agents and is outside the approved Brad-only scope. The job definition is privately backed up; its failed status and tool denial remain unchanged. No direct database edit or permission bypass is attempted. Pausing this job remains an owner decision about global behavior.

## Live result — October 7, 2026
The repair completed against OpenClaw 2026.9.8 (fc23bc8), with private rollback backup `/home/steve/.openclaw-career-backups/20261007T144733476393Z`. Exact comparison with the backup confirmed only Brad’s primary model and thinkingDefault changed. All other configuration is byte-equivalent at the parsed value level.

A real website conversation (`5e21b651-b70b-46f1-ac1e-4368224ed725`) passed chat, explicit response save/read, draft creation/save/read and unchanged primary-source hashes. Two successful real model requests used the existing provider chain. Native session metadata records provider `openai`, model `gpt-6.1-sol`, no model override and no session thinking override; medium comes from Brad’s validated agent default. No OpenRouter fallback was observed in this session. An earlier technical conversation failed while the gateway was starting, before an AI reply/save; it was not an acceptance pass.

Brad and Steve web services and backup timers remain active. Public OpenClaw `/v1/models` and `/v1/chat/completions` still return 404. Steve’s model and personal routing are unchanged. The existing immutable web release remains active; staged helpers are under `/home/codex-deploy/apps/career-ops-editor/upgrades/20261007-runtime-01/`.

The incompatible monitor remains enabled with lastRunStatus error. Installed native configuration supports `skills.workshop.autonomous.mode` values `auto`, `propose`, `off`; the scheduler enables system review monitors only for `auto`. Recommended next decision: use `propose` globally to stop autonomous reviews without expanding career tools. This also affects the personal agent, so it was not applied during the Brad-only repair.
