# Verification — October 3, 2026

A focused credential-pattern check of the 121 published implementation files found no provider-token or private-key matches. This is not a full history/secret audit. Live listeners were 127.0.0.1:3921, 127.0.0.1:3922 and loopback IPv4/IPv6:18789. Both public career Assistant endpoints and direct unauthenticated loopback APIs returned 401. An authenticated request with a foreign Origin returned 403 without a model call.

The existing OpenClaw owner hostname separately reverse-proxies port 18789. Its /v1/models and /v1/chat/completions currently return 401 without the gateway token. This is authenticated public reachability, not demonstrated credential leakage. The proposed additional restriction prevents these requests from reaching the gateway even if a client has a token. The owner dashboard proxy remains present.

Twelve portal tests passed, including restriction idempotence, original proxy preservation and refusal of unrecognized configuration. Installed Caddy accepted the proposed actual site configuration in non-mutating --check mode. Strict OpenSpec validation and whitespace checks passed. No AI provider was invoked, no credential was read for diagnostics, and no live Caddy change was made.

Owner activation:

```sh
sudo python3 /home/codex-deploy/apps/career-ops-editor/security/lock-openclaw-http.py
```

The helper saves the original site in a root-private /etc/career-ops backup, retains file ownership/mode, validates the full configuration and reloads Caddy. Validation/reload failure restores the previous site automatically. After activation, verify public /v1 API requests return 404, hosted Assistant still loads and answers, and the existing owner dashboard remains usable. No repository visibility change is needed for this runtime restriction.
