## Latest usability update: Save response

After assistant-02 is active, activate the qualified code-only response-saving release:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-responses-01/portal/deploy/activate-assistant-responses.py
```

Reload Assistant and use Save response beneath any completed reply, including replies from older conversations. It saves the exact reply as review material in output/assistant with a download link and live Documents visibility, without a model call. Repeated saves reuse the identical file; independently modified exports are not overwritten. Create a document draft in Operation generates new documents. The helper preserves the existing OpenClaw agents, credential reference and provider chain. Rollback uses the same command with --rollback and retains saved documents/conversations.

# Career Assistant activation and acceptance

This release uses version-qualified bounded agents in Steve’s existing OpenClaw gateway. The installed identity-owned subscription credentials are reused through that runtime; no credential/account or personal conversation store is copied into career agents. Only the server selects agents and conversation keys. All native model tools are denied. The app applies a closed operation protocol through existing revision/history/canonical helpers.

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-02/portal/deploy/activate-assistant.py
```

The helper backs up private runtime/unit/env configuration in a root-only journal, validates the installed OpenClaw version/schema, preserves the main agent and personal provider chain, adds explicit main owner routes needed by a multi-agent fleet, enables private HTTP chat, and switches qualified web code. It makes no model request. Career agents use the existing OpenAI-first/OpenRouter-second chain. Steve’s OpenRouter account limit controls spending; there is no app-level spending gate. Semantic memory/embedding lookup and scheduled career heartbeats are disabled. The personal assistant’s existing configuration is untouched.

After activation, verify the existing personal Telegram assistant still routes to main. Open Assistant in both browser workspaces. Begin with a fictional question or existing-source discussion before authorizing edits. A live trial using the approved provider chain and actual candidate grounding/usability acceptance are separate evidence; fake-provider qualification does not prove model quality or credential eligibility for newly targeted agents. OpenRouter fallback is approved under Steve’s account limit. Do not introduce a new API key or alternate provider chain.

Test draft generation, immediate Documents visibility, source-backed explicitly requested edits, conflict preservation, reconnect and cancellation. The operation selector defines the permitted write for a request; Discuss is read-only. New claims still require explicit confirmed candidate statements. No applications/messages are sent and no Applied status is automatic. Shared-login attribution remains honest.

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261003-assistant-02/portal/deploy/activate-assistant.py --rollback
```

Rollback restores earlier web/service and OpenClaw configuration while retaining candidate documents and conversations. Private journals include configuration secrets and must never be copied to the repo or served.

The October 3 activation repair supports the existing built-in store SecretRef through the pinned installed native resolver, run as Steve. Its output is captured privately by the root activation process, never displayed. The original gateway reference stays unchanged; only the private career service environment receives the resolved token. Unsupported references stop before activation.
