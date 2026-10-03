## ADDED Requirements

### Requirement: Live and archived document inventory
The system SHALL list candidate-specific current VPS documents and historical snapshot documents with source, type and modification date.

#### Scenario: Newly saved report
- **WHEN** a search writes a report to the candidate data root
- **THEN** the next library refresh shows that report without daily publication or copying from the Mac

#### Scenario: Archived document
- **WHEN** a previous snapshot contains a document also present in current data
- **THEN** both copies appear with distinct Current and Archive labels

### Requirement: Bounded read-only document access
The system SHALL provide validated candidate-scoped viewing and downloads without exposing private runtime or executing document HTML.

#### Scenario: Unsafe request
- **WHEN** a caller requests another candidate's ID or a path traversal, hidden credential file or nested checkout
- **THEN** the request is refused and candidate files are unchanged

### Requirement: Mobile filters and navigation
The library SHALL support keyword, source, type and date filters in phone browsers.

#### Scenario: Today
- **WHEN** the visitor selects today's current documents
- **THEN** the date and current-source filters apply while a Show all documents control restores the complete inventory
