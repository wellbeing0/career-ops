## ADDED Requirements

### Requirement: Browser career conversations
The system SHALL provide a mobile Assistant interface inside the authenticated candidate workspace without requiring Codex desktop or Telegram.

#### Scenario: Continue a conversation
- **WHEN** a user reopens a candidate conversation after disconnecting
- **THEN** messages and confirmed operation outcomes are restored without replaying completed edits

#### Scenario: Select another candidate
- **WHEN** the user changes from Brad to Steve
- **THEN** the assistant selects a distinct candidate-bound conversation and tool context

### Requirement: Private OpenClaw integration
The system SHALL use an installed-version-qualified private server adapter with server-selected agent and conversation identifiers and SHALL keep operator credentials out of browser responses.

#### Scenario: Browser attempts routing override
- **WHEN** a request supplies another agent, arbitrary session key, model override or scope
- **THEN** the server rejects or ignores it according to the fixed career policy rather than broadening authority

#### Scenario: Runtime lacks documented support
- **WHEN** the installed gateway does not support the proposed transport or bounded tools
- **THEN** activation stops and the limitation is reported without changing the personal assistant to conceal it

### Requirement: Bounded candidate tools
The assistant SHALL access only the selected candidate’s permitted career tools and SHALL NOT expose arbitrary shell, path, secret, administration, cross-candidate conversation or personal messaging capabilities.

#### Scenario: Hostile job posting
- **WHEN** external job content instructs the assistant to reveal credentials or change rules
- **THEN** it is treated as untrusted job data and cannot trigger privileged operations

#### Scenario: Cross-candidate access
- **WHEN** Brad’s bound conversation requests Steve’s conversation or an unapproved filesystem path
- **THEN** the tool boundary refuses it regardless of model output

### Requirement: Source-backed content
The assistant SHALL use approved primary files and direct confirmed candidate statements for factual claims and SHALL preserve source provenance.

#### Scenario: Missing accomplishment detail
- **WHEN** a requested CV change requires an unsupported metric or authorship claim
- **THEN** the assistant asks for confirmation or the correct detail and omits unconfirmed claims

### Requirement: Authorized recoverable saves
The system SHALL save explicitly requested supported edits through current revision checks and automatic previous-version history, and SHALL make generated drafts visible in live Documents.

#### Scenario: Explicit routine edit
- **WHEN** the user requests a supported edit within established authority and the revision is current
- **THEN** the validated edit saves with automatic history without a redundant approval step

#### Scenario: Concurrent profile update
- **WHEN** another session changed the source revision before the assistant saves
- **THEN** the edit is refused, the proposed text is retained and the user can compare before retrying

#### Scenario: Interrupted save reply
- **WHEN** the connection drops after a save may have completed
- **THEN** the operation ledger determines the outcome before any retry and prevents duplicate writes

### Requirement: Provider order and paid fallback control
The system SHALL preserve the verified VPS OpenAI-first/OpenRouter-second configuration and rely on Steve’s existing OpenRouter account limit without an app-level spending gate.

#### Scenario: Primary unavailable
- **WHEN** the primary provider is unavailable and the configured fallback is selected
- **THEN** OpenClaw uses the existing OpenRouter fallback under the account-level limit

#### Scenario: Provider rejects a request
- **WHEN** the provider rejects the request, including account-limit failures
- **THEN** the run records a safe failure and retains the conversation for retry without adding another provider

### Requirement: Human-reviewed job process
The assistant SHALL keep application material as drafts and SHALL NOT submit applications, send outreach or automatically mark a job Applied.

#### Scenario: Create application packet
- **WHEN** a user requests a tailored resume and application draft
- **THEN** draft files are saved to the candidate output area with review links and no external submission

### Requirement: Honest attribution and reversible activation
The system SHALL label shared-login operations honestly and SHALL support disabling AI without losing documents, histories or existing personal OpenClaw functionality.

#### Scenario: Shared login edit
- **WHEN** an edit is made under the existing shared login
- **THEN** its audit identifies shared-login and the selected candidate without asserting individual identity

#### Scenario: Roll back AI
- **WHEN** the owner disables or rolls back the career assistant
- **THEN** existing profile editing, search, pipeline and Documents remain usable and completed candidate files are retained

### Requirement: Save completed conversation responses
The system SHALL let the user save a completed assistant reply verbatim from its message card without another model call, preserve candidate isolation and link the saved Markdown document into live Documents. Saved discussion SHALL be labeled as AI output for review, not a verified primary source.

#### Scenario: Save and retrieve a discussion
- **WHEN** the user presses Save response on a completed reply
- **THEN** the server exports that existing candidate-bound reply and returns a download link, including after a page reload

#### Scenario: Retry or modified saved document
- **WHEN** the same reply is saved again after an uncertain request
- **THEN** the existing identical export is reused, while an independently modified document is retained without overwriting
