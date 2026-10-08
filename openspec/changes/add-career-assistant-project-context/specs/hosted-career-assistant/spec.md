## ADDED Requirements
### Requirement: Deployment-coherent project knowledge
Every hosted assistant turn SHALL receive reviewed project guides matching the deployed release, with repository identity, exact source commit and validated document hashes.
#### Scenario: Project help question
- **WHEN** a candidate asks which repository runs the site or how search works
- **THEN** the assistant receives the deployed product guide independently of candidate facts and native tool availability
### Requirement: Bounded isolated operational context
Each turn SHALL receive a timestamped read-only selected-candidate workspace snapshot with search counts/source outcomes, filters, pipeline summaries and application status counts. Limits and unavailable data SHALL be explicit.
#### Scenario: Empty search diagnosis
- **WHEN** a candidate asks why no new matches appeared
- **THEN** the assistant receives available found/filtered/duplicate counts and source failures without changing search state or reading another candidate
### Requirement: Context preserves factual authority
Project and operational data SHALL NOT become candidate accomplishments or broaden save/tool authority.
#### Scenario: Unsupported numerical resume claim
- **WHEN** a number exists only in project or operational context
- **THEN** it cannot justify saving that number as a candidate achievement
