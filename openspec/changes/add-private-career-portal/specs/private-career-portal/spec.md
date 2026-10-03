## Purpose

Provide private, read-only access to existing job-search documents for two explicitly selected candidates, with authenticated downloads and recoverable snapshot publication.

## ADDED Requirements

### Requirement: Entire site requires the shared login
The deployed site SHALL require one shared login over HTTPS for every candidate page, asset and original download. Credentials SHALL remain outside the served tree and source repository.

#### Scenario: Unauthenticated document request
- **WHEN** a visitor requests a candidate document without valid credentials
- **THEN** the server returns an authentication challenge and no document content

#### Scenario: Authenticated navigation
- **WHEN** a visitor supplies valid shared credentials
- **THEN** the visitor can browse either candidate directory and download its published documents

### Requirement: Explicit candidate ownership and read-only behavior
The portal SHALL build separate directories from explicit candidate roots, retain attribution, and expose no editing, task execution or application submission endpoints.

#### Scenario: Candidate separation
- **WHEN** a visitor opens one candidate directory
- **THEN** its document catalog contains only that candidate's selected files

#### Scenario: Mutation request
- **WHEN** a client attempts to write or execute through the site
- **THEN** no user-layer file changes and no career-ops process starts

### Requirement: Pertinent documents are available with provenance
The portal SHALL include available profiles, CVs, original resumes, evaluations, search and tracker documents, application samples, interview preparation and pertinent job-search notes. It SHALL display snapshot time, source modification times and draft/stale-source notices, and preserve original downloadable content. It SHALL exclude credentials, caches, code, raw fetch receipts, migration archives and recovery backups. It SHALL reject symlink escapes and secret-pattern content in selected text documents rather than silently publishing them.

#### Scenario: Read or download a document
- **WHEN** a visitor selects a published Markdown or text document
- **THEN** the portal displays escaped readable content with candidate attribution and a link to the unchanged original

#### Scenario: Excluded or escaped source
- **WHEN** discovery encounters a backup, executable, credential file or symlink outside a candidate root
- **THEN** it is absent from the served catalog and an escape or selected credential-content finding fails the build

### Requirement: Publication is atomic and recoverable
The publisher SHALL create an immutable release with a hash manifest outside the served tree, verify its contents and activate through one symlink replacement. The existing release SHALL remain available if transfer or validation fails. Runtime credentials SHALL survive document updates.

#### Scenario: Interrupted publication
- **WHEN** a new release is incomplete or its manifest fails validation
- **THEN** activation fails and the previous current release remains served

#### Scenario: Rollback
- **WHEN** an operator selects a previously verified release
- **THEN** that complete snapshot is restored without modifying credentials or local candidate source files

### Requirement: Administrator handoff preserves other sites
The installer SHALL add only the designated Caddy site and its private authentication fragment, validate the complete configuration before reload, and preserve unrelated routing. Live acceptance SHALL remain pending until authenticated and unauthenticated probes pass after administrator setup.

#### Scenario: Invalid Caddy configuration
- **WHEN** full Caddy validation fails after installing the candidate site configuration
- **THEN** the installer restores its prior site configuration and does not reload the invalid configuration
