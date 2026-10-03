## Why
The owner wants his OpenClaw-backed career AI restricted to the current hosted application while the repository stays public. The published code contains no detected credentials. Career endpoints require shared authentication and foreign-origin requests are rejected. However, the existing public OpenClaw owner portal proxies the gateway, including its newly enabled OpenAI-compatible HTTP endpoints. Those endpoints require bearer authentication but can be blocked from public proxying entirely.

## What Changes
Block /v1 and /v1/* on the public OpenClaw hostname with an explicit Caddy response. Preserve local gateway access, the authenticated Career Ops endpoints and the owner dashboard proxy. Provide a reversible sudo installer with backup and validation.

## Impact
No application code, candidate data, provider identity or spending settings change. The public repository remains public. The runtime token remains private. Administrator activation and subsequent live checks are separate from syntax qualification.
