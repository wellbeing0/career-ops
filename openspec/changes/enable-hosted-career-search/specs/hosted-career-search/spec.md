## Purpose

Let candidates search public job boards from their hosted workspace, retain meaningful results across phone sessions, and build a source-backed preliminary shortlist.

## ADDED Requirements

### Requirement: Candidate-scoped search navigation
The system SHALL provide a mobile-accessible Search entry in each authenticated workspace and SHALL derive storage and execution roots from server-owned candidate configuration.

#### Scenario: Candidate workspace selection
- **WHEN** a visitor enters Brad's Search page
- **THEN** searches and publication operate only on Brad's configured root, even if a request supplies another candidate or file path

### Requirement: Free bounded preview
The system SHALL preview configured supported public job boards without paid model calls or sending candidate documents to providers, SHALL respect blacklist and dedup policies, and SHALL enforce a displayed time limit, result cap and concurrency bound without updating canonical pipeline files during preview.

#### Scenario: Limit reached
- **WHEN** a scan reaches a time or result limit
- **THEN** the saved run is marked partial with the limit identified and available results remain reviewable

### Requirement: Durable job lifecycle
The system SHALL retain candidate-specific run receipts and results across browser disconnections, prevent duplicate starts for the same request, permit cancellation, and distinguish queued, running, completed, partial, failed, cancelled and interrupted outcomes.

#### Scenario: Phone reconnects
- **WHEN** a visitor closes the browser during a running search and later returns
- **THEN** the visitor can see the same run and its current state and results without starting another search

#### Scenario: Service restarts
- **WHEN** a service restarts with an unfinished search
- **THEN** the retained receipt shows interruption or verified resumption and does not claim completion without evidence

#### Scenario: Cancel requested
- **WHEN** a visitor cancels an active search
- **THEN** owned search work stops, partial results remain labeled, and unrelated processes are unaffected

### Requirement: Honest source coverage
The system SHALL show per-source success, failure, freshness and coverage information and SHALL distinguish a successful empty search from unavailable sources or malformed candidate targeting.

#### Scenario: All boards unavailable
- **WHEN** every requested board fails
- **THEN** the run reports source failure and does not present zero results as evidence that no matching jobs exist

### Requirement: Preliminary ranking with provenance
The system SHALL label free rankings preliminary, explain ranking signals, retain source URLs and retrieval times, and distinguish known criteria from unknown salary, benefits, location, travel and eligibility. It SHALL NOT present title fit as an AI evaluation or as proof of full profile compliance.

#### Scenario: Salary omitted
- **WHEN** a title fits the candidate but the posting omits compensation
- **THEN** the result can appear in the shortlist with compensation unknown and does not count as verified above the salary minimum

#### Scenario: Profile changes
- **WHEN** the candidate updates targeting after a search starts
- **THEN** the run retains its original targeting revision and displays that newer targeting exists

### Requirement: Explicit canonical publication
The system SHALL publish only explicitly selected server-held offers through canonical pipeline and scan-history writers, retain a publication receipt, prevent duplicated effects on retry, and SHALL NOT mark applications submitted or Applied as a result of selection.

#### Scenario: Tampered offer selection
- **WHEN** a client supplies an invented offer payload or another candidate's result identifier
- **THEN** publication is rejected without writing candidate files

#### Scenario: Publication interrupted
- **WHEN** selection publication fails or is interrupted
- **THEN** existing results remain available and retry reconciles canonical writes without creating duplicates

### Requirement: Editing and backup compatibility
The system SHALL serialize canonical publication with hosted editing and backups, preserve history and source revisions, and keep runtime caches out of document exports while retaining recoverable run receipts.

#### Scenario: Save or backup during selection
- **WHEN** an edit or backup overlaps selected-offer publication
- **THEN** operations observe a coherent candidate state without missing publication files or corrupting edit history

### Requirement: Controlled network and content boundary
The system SHALL treat postings as untrusted data, enforce authenticated same-origin mutations and supported public-provider destination restrictions, and SHALL NOT enable arbitrary commands, generic AI workers, submission or outreach through search routes.

#### Scenario: Posting contains agent instructions
- **WHEN** posting text asks the system to change rules, expose secrets or execute actions
- **THEN** the text remains posting data and triggers none of those actions

#### Scenario: Private network destination
- **WHEN** a request or redirect targets a private or local network address
- **THEN** fetching is rejected and the run records the source error without accessing that address
