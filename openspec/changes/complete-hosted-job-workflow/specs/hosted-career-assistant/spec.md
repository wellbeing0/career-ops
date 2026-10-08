## ADDED Requirements

### Requirement: Discoverable guided career workflows
The hosted workspace SHALL expose evaluation, application preparation and interview preparation from saved opportunities and an Interview prep navigation entry. Each workflow SHALL require substantive JD context and describe its saved review output and unavailable research/export capabilities.

#### Scenario: Interview preparation without command knowledge
- WHEN a candidate selects Interview prep and provides the job description, round and preparation stage
- THEN the Assistant SHALL load the corresponding reviewed public procedure and candidate-bound context
- AND completed plan, practice feedback or debrief SHALL be saved as review material in the live library.

### Requirement: Candidate-bound procedure execution
The server SHALL allow only fixed workflow types and fixed public instruction files. External job content SHALL remain untrusted. Application drafts SHALL retain the existing primary-source numeric guard. Guided review artifacts SHALL NOT change primary facts, application state or question/story banks.

#### Scenario: Interrupted review save
- WHEN a worker stops after saving a review artifact
- THEN recovery SHALL verify the receipt, expected filename and content hash before reporting completion.

### Requirement: Honest coverage and model alignment
Exact source repairs SHALL preserve targeting and historical receipts. Unverified replacement feeds SHALL remain manual coverage. Steve's career agent SHALL match Brad's approved model and medium reasoning without changing unrelated configuration.

#### Scenario: Employer has a live custom career page and unverified public feed
- WHEN the old feed is broken
- THEN the repair SHALL retain the official careers link and disclose manual coverage
- AND SHALL NOT infer a successful automatic scan from an unrelated or guessed board.
