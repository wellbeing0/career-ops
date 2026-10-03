## ADDED Requirements

### Requirement: Clear live pipeline navigation
The workspace SHALL expose a Pipeline tab for saved opportunities, distinguish application records from job selections, and label profile/CV History as recovery.

#### Scenario: Selected search result
- **WHEN** the visitor adds a search result to the pipeline and opens Pipeline
- **THEN** the saved opportunity is visible from VPS data without manual synchronization

#### Scenario: Recovery navigation
- **WHEN** the visitor opens Profile/CV recovery
- **THEN** the interface explains that search history is under Search and saved opportunities are in Pipeline

### Requirement: Source-attributed job review note
The system SHALL preserve an owner-stated job review separately from unverified role eligibility.

#### Scenario: Grafana review
- **WHEN** the owner-stated global and remote-first review is recorded
- **THEN** the saved opportunity shows the attributed note without claiming Michigan eligibility is confirmed
