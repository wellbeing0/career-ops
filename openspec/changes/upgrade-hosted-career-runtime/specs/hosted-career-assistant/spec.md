## ADDED Requirements

### Requirement: Explicit candidate model defaults
Brad’s website agent SHALL select openai/gpt-6.1-sol with medium reasoning independently of console-session overrides, preserving its configured fallback and security policy.

#### Scenario: New website conversation
- **WHEN** a new Brad conversation is started through Career Ops
- **THEN** the selected agent uses the configured GPT-6.1 Sol / medium defaults unless an approved session override exists

### Requirement: Version-qualified maintenance
Installation helpers SHALL use only explicitly qualified installed versions and resolver mappings. Existing reviewed agents SHALL retain their chosen models and reasoning defaults.

#### Scenario: Unknown upgrade
- **WHEN** a runtime version has no qualified mapping
- **THEN** installation refuses before reading a gateway credential or changing services

### Requirement: Incompatible maintenance remains bounded
A maintenance task that requires denied career tools SHALL be paused with its original definition retained rather than broadening tool permissions.

#### Scenario: Skill review requires filesystem tools
- **WHEN** the identified career-brad maintenance job cannot operate under deny-all tools
- **THEN** it is disabled, retained in a private backup and reported as paused

#### Scenario: Runtime forbids candidate-scoped pause
- **WHEN** the installed runtime makes this a system-owned monitor editable only through global configuration
- **THEN** the original definition is privately retained, tool denial remains unchanged and the global decision is reported as unresolved; other authorized repairs proceed
