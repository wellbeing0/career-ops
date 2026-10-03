## Purpose

Allow authenticated visitors to edit the correct candidate's career profile, master CV and existing tracker records on an authoritative VPS while preserving canonical files, preventing lost updates and providing recovery.

## ADDED Requirements

### Requirement: VPS authority is explicit
After cutover the system SHALL use VPS candidate files as the source of truth. Mac copies SHALL be identified as backups or exports. A publication or code deployment SHALL NOT overwrite live candidate data.

#### Scenario: A Mac copy is stale
- **WHEN** an operator attempts to deploy code or republish a static snapshot from an older Mac dataset
- **THEN** live VPS candidate files remain unchanged and the snapshot is identified as historical rather than current authoritative data

### Requirement: Shared authentication preserves candidate boundaries
The system SHALL retain the shared login and require it for every page, API and download. Each workspace SHALL show its candidate identity and resolve a fixed server-owned data root. Client paths, headers and cookies SHALL NOT choose arbitrary filesystem roots. The service handling one candidate SHALL NOT have access to the other's private data.

#### Scenario: Simultaneous candidate tabs
- **WHEN** a visitor edits different candidates in separate tabs
- **THEN** each request remains bound to its workspace path and no global active-candidate cookie redirects an edit into the other root

#### Scenario: Unauthorized or forged request
- **WHEN** a request lacks valid login, has an unapproved origin or supplies a forged candidate root
- **THEN** it is rejected without reading or changing private data

### Requirement: Hosted capabilities are enforced on the server
The initial hosted-editing mode SHALL permit only required reading, profile/CV edits, existing tracker status/notes updates and authorized revision recovery/export. It SHALL reject worker execution, scans, ingestion, provider configuration, application automation and destructive/bulk tracker operations regardless of visible controls or HTTP method.

#### Scenario: A hidden API is called directly
- **WHEN** a visitor requests a disabled scan, AI assistant, application, ingestion or deletion endpoint
- **THEN** the server refuses it and no worker, provider call, browser session or data mutation occurs

### Requirement: Profile edits preserve facts and targeting coherence
The system SHALL provide non-AI profile editing for identity/contact, target roles, base-pay minimum/target, location/travel and work-authorization fields, plus explicit review/editing of narrative personalization. It SHALL preview changes, validate existing YAML without template reset, preserve unrelated fields and source provenance, and prevent conflicting targeting facts between structured profile and personalization files from silently becoming active.

#### Scenario: A salary preference changes
- **WHEN** a visitor saves a new base minimum or target
- **THEN** the exact canonical minimum and target fields reflect the change, benefits/bonus/equity remain separate, and recognized duplicate targeting sections are automatically reconciled with the saved structured fields, and their originals remain recoverable in history

#### Scenario: Existing profile is malformed
- **WHEN** a profile file cannot be parsed or is not a mapping
- **THEN** the editor reports the error and preserves the original rather than seeding a template or replacing it

### Requirement: CV edits are explicit candidate-authored changes
The system SHALL preview the master CV and show the current revision before a save. It SHALL preserve employment titles and facts unless the visitor explicitly changes them. It SHALL NOT generate achievements, silently add missing stack keywords or turn derived/unconfirmed metrics into established facts.

#### Scenario: Candidate supplies an accomplishment
- **WHEN** a visitor edits CV text and confirms the save
- **THEN** only that candidate's master CV changes, the prior revision remains recoverable and saved content is shown immediately

### Requirement: Concurrent changes cannot silently overwrite each other
Writes SHALL carry a revision precondition checked within the relevant write lock. Stale edits SHALL return a visible conflict with reload/compare choices and retain unsaved browser text. Multi-file profile saves SHALL have recoverable intent and revision records so interruption cannot leave conflicting targeting active.

#### Scenario: Two tabs edit the same CV
- **WHEN** a second tab saves against an outdated revision after the first tab succeeds
- **THEN** the second save is refused without replacing the newer CV and its unsaved text remains available

### Requirement: Tracker writes reuse canonical operations
Existing tracker status and note updates SHALL delegate to the core's canonical validated/locked writer, with row identity and revision checks performed under that lock. Status changes SHALL retain the standard transition ledger. The hosted app SHALL NOT rewrite the entire tracker from a stale browser table or mark an application sent as a consequence of browsing or drafting.

#### Scenario: A tracker status changes
- **WHEN** a visitor confirms a permitted status for an existing row at its current revision
- **THEN** the canonical core operation updates that candidate's row and ledger without dropping another writer's changes

#### Scenario: The row has changed since display
- **WHEN** row identity or revision no longer matches the visitor's selected record
- **THEN** no tracker mutation occurs and the interface requests a refresh

### Requirement: Changes are recoverable without invented identity
The system SHALL retain private versioned revisions and scheduled dataset backups outside the served tree, support export and explicit revision restore, and record candidate, timestamp, operation and resulting revision. With the shared login it SHALL label the authenticated principal as shared rather than claim verified individual authorship. Restore SHALL create a new revision and never delete prior history.

#### Scenario: Restore an earlier CV
- **WHEN** a visitor previews and confirms an earlier revision
- **THEN** that content becomes a new current revision with an audit event and the previous current content remains recoverable

### Requirement: Live and snapshot content are distinguished
The portal SHALL retain historical documents and the two candidate directories while clearly distinguishing authoritative live profile/CV/tracker views from dated snapshots. An edit SHALL NOT rewrite archived evaluations, samples or job descriptions as though they had been freshly generated.

#### Scenario: A profile changes after a sample application was generated
- **WHEN** the visitor opens the older sample
- **THEN** its original date/content remain intact and the interface indicates that it predates the latest profile revision

### Requirement: Migration and rollback preserve new edits
Cutover SHALL verify complete candidate datasets and backups before enabling edits. A failed deployment SHALL leave the viewing portal available. Code rollback SHALL preserve live edited data; data restoration SHALL require an explicit selection and never silently restore the initial Mac snapshot.

#### Scenario: A release is rolled back after browser edits
- **WHEN** an operator returns to the prior application version
- **THEN** successfully saved candidate edits remain in the authoritative dataset and incompatible editing is disabled rather than discarding data

### Requirement: Ordinary saves require no separate approval gate
The system SHALL accept a valid profile, CV or existing-row tracker edit when the visitor presses Save, without an initial targeting-review gate or an additional save confirmation. It SHALL automatically checkpoint prior versions and synchronize recognized targeting sections. Restore and explicit discard may retain confirmations. Saving one tab SHALL preserve unsaved drafts in other tabs, and conflicts SHALL retain the draft without overwriting newer source files.

#### Scenario: First profile edit
- **WHEN** a visitor edits a profile that has no managed targeting block and presses Save
- **THEN** the system backs up the original profile and narrative, saves the fields, and generates consistent targeting automatically

#### Scenario: CV draft while saving a profile
- **WHEN** a visitor has an unsaved CV draft and saves a profile change
- **THEN** the CV draft remains in the editor and only the submitted profile changes are written
