## ADDED Requirements

### Requirement: Simple workflow re-entry page
The authenticated site index SHALL show Brad and Steve workspace choices, concise job-search steps, feature explanations and return-visit shortcuts, with phone-friendly controls and system light/dark theme.

#### Scenario: Candidate returns after a break
- **WHEN** the candidate opens the site index
- **THEN** they can choose their live workspace or Search, Pipeline or Assistant without interpreting archive dates or restarting onboarding

### Requirement: Coherent and reversible publication
Publication SHALL preserve archive documents and shared authentication, refresh Assistant guides with a version/hash manifest, and offer rollback without changing candidate data.

#### Scenario: Start-page release is activated
- **WHEN** the owner activates the qualified start-page release
- **THEN** the new index and matching Assistant context are active and prior releases remain recoverable
