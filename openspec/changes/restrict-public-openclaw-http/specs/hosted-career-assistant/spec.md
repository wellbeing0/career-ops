## ADDED Requirements

### Requirement: Local-only OpenClaw HTTP AI API
The public OpenClaw reverse proxy SHALL refuse /v1 and /v1/* requests while the Career Ops server SHALL continue accessing the authenticated gateway through loopback. Repository visibility SHALL NOT supply runtime credentials.

#### Scenario: Public model API request
- **WHEN** a client requests /v1/models or /v1/chat/completions on the public OpenClaw hostname
- **THEN** Caddy responds 404 without forwarding the request to OpenClaw

#### Scenario: Hosted career request
- **WHEN** an authorized request arrives through the Career Ops application
- **THEN** the selected candidate adapter can continue using its private authenticated loopback connection
