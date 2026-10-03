## ADDED Requirements

### Requirement: Existing opportunities remain visible
The system SHALL show previously saved pipeline and added scan-history opportunities alongside new search results, with safe posting links and unverified freshness.

#### Scenario: No new jobs
- **WHEN** a scan contains only duplicates
- **THEN** the visitor can view existing opportunities and see that zero new matches does not mean zero opportunities

### Requirement: Candidate filter editing
The system SHALL allow candidate-specific job-filter viewing, editing and restoration with validation, conflict protection and automatic previous-version backup.

#### Scenario: Conflicting edits
- **WHEN** portals settings change after loading
- **THEN** a stale save is refused and current settings remain intact

#### Scenario: Save filters
- **WHEN** valid filters are saved
- **THEN** unrelated settings remain intact and subsequent scans use the saved filters
