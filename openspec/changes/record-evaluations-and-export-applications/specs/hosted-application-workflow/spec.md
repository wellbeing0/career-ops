## ADDED Requirements

### Requirement: Reviewed evaluation registration
The hosted workspace SHALL allow explicit registration of a current hosted evaluation as a numbered report and Evaluated tracker row with reviewed job fields, preserved JD and original document, shared tracker locking, duplicate protection, private prior-version backup and interrupted-write recovery.

#### Scenario: Candidate records a reviewed evaluation
- **WHEN** the candidate submits reviewed company, role, URL and optional score for a current hosted evaluation
- **THEN** one numbered report and one Evaluated row are recorded and no application is submitted

#### Scenario: Interrupted registration is retried
- **WHEN** registration stops between durable writes and the same registration is retried
- **THEN** the journal completes the same row/report without duplicate records or overwriting unrelated changes

### Requirement: Candidate-bound quality review and PDF export
The workspace SHALL provide a quality review and explicit acknowledged PDF save for current Markdown CV/application documents, with full-document/resume-only choices, honest ATS/fact/title findings, input-change refusal and candidate-local immutable artifacts.

#### Scenario: Packet resume is exported
- **WHEN** a candidate chooses its recognized resume section, reviews checks and acknowledges review
- **THEN** a text-based PDF and check notes appear in Documents without changing the master CV or Applied status

#### Scenario: Input changes after review
- **WHEN** source, primary evidence or selected evaluation changes after the quality review
- **THEN** export is refused until the candidate refreshes the checks

#### Scenario: Check coverage is incomplete
- **WHEN** titles or keywords cannot be extracted reliably
- **THEN** findings explicitly report unavailable or incomplete coverage rather than claiming a clean pass
