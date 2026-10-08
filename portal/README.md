# Hosted Career Ops

The hosted system provides two candidate workspaces behind shared authentication: profile/CV editing with version history, free ATS job searches and editable filters, pipeline updates, a live document library and an OpenClaw-backed career Assistant. Candidate data is authoritative on the VPS and separate from this repository; local candidate copies are backups. Never commit candidate files, provider credentials, authentication files or runtime histories.

The Assistant supports candidate-bound conversations, explicit supported edits, document drafts and saving completed replies. Application submission and outreach remain human actions. OpenClaw uses the existing OpenAI-first/OpenRouter-fallback chain, with spending controlled by the owner’s OpenRouter account limit. Current candidate agents deny native model tools; application actions use bounded server helpers.

See `openspec/changes/` for phase requirements and verification evidence, and `portal/deploy/` for release-specific administrator handoffs. The latest accepted code release is `20261003-assistant-responses-01`. Deployment scripts contain server layout assumptions and release-specific paths; adapt and qualify them before reuse on another host. Candidate data migration is separate from code activation.

## Development checks

```sh
npm --prefix web test
npm --prefix web run typecheck
python3 -m unittest discover -s portal/tests
```

Browser qualification helpers use fictional candidate roots and local non-billing provider stubs. Passing them does not establish live model quality or authorize a new deployment. Generated builds, node_modules, private data pointers and deployment credentials remain ignored.

The following describes the original viewing-only phase and its retained archives.

# Private Career Ops viewing portal

Phase 1 exports private candidate files into a static snapshot. It does not run the alpha `web/` application, write candidate data, launch model workers or submit applications.

## Build and verify

Use explicit roots and keep the output outside this repository and outside both candidate roots:

```sh
python3 portal/build.py \
  --candidate steve=/absolute/private/steve \
  --candidate brad=/absolute/private/brad \
  --output /absolute/private/releases/UNIQUE_RELEASE_ID
python3 -m unittest discover -s portal/tests -v
```

Each release contains `site/` and a private `manifest.json`. The manifest is NOT served. It records hashes and omitted paths/reasons. Original selected files are byte-preserving; previews escape Markdown/text and sandbox HTML. CSP disables source HTML scripts and external embeds. Original PDFs and Word files are offered as authenticated downloads. Displayed documents retain draft and source-date warnings.

The publisher selects readable document types from profile/config/modes, data, reports, output, documents, interview preparation and writing samples. It excludes code, JSON fetch receipts, hidden/runtime files, migrations and backups. Pertinent job-search notes are included under the explicitly authorized shared-visibility model. Do not store credentials in document areas; detected credential-pattern content fails the build.

## VPS layout and publication

- Application home: `/home/codex-deploy/apps/career-ops-portal`
- Releases: `releases/UNIQUE_RELEASE_ID/{site,manifest.json}`
- Current snapshot: `current` symlink into `releases/`
- Administrator installer: `deploy/install-caddy.sh`
- Permanent Caddy site: `/etc/caddy/conf.d/careerops.steveleclair.info.caddy`
- Private authentication: `/etc/caddy/private/careerops-auth.caddy` (`root:caddy`, 0640)

Transfer the complete release to a new release directory, then verify and atomically activate:

```sh
python3 /home/codex-deploy/apps/career-ops-portal/deploy/activate.py \
  --base /home/codex-deploy/apps/career-ops-portal --release UNIQUE_RELEASE_ID
```

The same command with an earlier release ID performs rollback. It verifies all hashes and refuses unexpected served files. It never edits authentication or local candidate documents. Retain previous releases until owner acceptance; no automatic deletion is enabled.

## Permanent administrator setup

Run on the VPS from a sudo-capable administrator account:

```sh
sudo bash /home/codex-deploy/apps/career-ops-portal/deploy/install-caddy.sh careerops.steveleclair.info
```

On first run it asks interactively for a shared username and a new password of at least 8 characters. It hashes the password using Caddy and keeps only its hash in a root-owned private fragment. The password is not passed as a process argument, printed or saved into the release. A rerun retains the existing shared login. Store the password in a password manager and share it directly with the other user; do not send it through chat or commit it.

The installer verifies the staged snapshot, checks Caddy read access and the existing conf.d import, backs up only this site's previous configuration, validates the entire Caddy configuration and reloads. Validation/reload failures restore the prior site file. Existing sites are not rewritten. The dedicated site requires authentication before serving content, rejects methods other than GET/HEAD, disables caching, and supplies a restrictive CSP. Caddy manages HTTPS certificates.

## Live acceptance after administrator setup

Check HTTPS, then request `/`, each candidate directory and a representative original download without credentials: all must challenge with 401. Test valid login in a browser; do not put the password in tool calls or shell history. Confirm both catalogs, source-document views and original downloads. Attempt POST with the authenticated session: 405, no mutation. Requests for `/manifest.json`, credential paths and omitted archives must not expose data. Inspect private login file ownership/mode. Archive OpenSpec only after live checks pass; successful staging is not live acceptance.

## Future interactive migration

A separate OpenSpec change should qualify candidate-specific upstream web instances, canonical-script edits and backups first; then VPS model/CLI authentication, worker isolation, queue/cancellation and explicit spend caps. Remote browser application assistance is another qualification step and retains manual human submission. Current publication does not activate those capabilities or transfer provider credentials.

## Deployment-coherent Assistant knowledge

`portal/knowledge/` contains the reviewed product guides supplied to both career assistants. These explain the repository, hosted workflows and capabilities; they never establish candidate facts. Each turn adds a timestamped, bounded read-only snapshot of only the selected candidate’s filters, latest search coverage/counts, saved opportunities and application status counts. Snapshot limits and unavailable data are explicit. Native model tools remain denied.

Package a release from a clean, committed checkout:

```sh
python3 portal/deploy/package-editor.py /absolute/staging/directory --release UNIQUE_RELEASE_ID
```

The package includes a knowledge manifest with the exact source commit, release ID and document hashes. Qualification and activation must verify it alongside source/build hashes. Copy guides with the code release, and roll them back with that release; do not independently pull GitHub main into the live assistant. Missing guides are identified as unavailable rather than represented as current project knowledge. Local development without a manifest is explicitly labeled as development.

### Hosted capability review and guided workflow increment

See [repository-to-website review](../docs/hosted-capability-review.md) for what is exposed, what is missing and why some CLI workflows should remain owner-only. The `complete-hosted-job-workflow` OpenSpec implements the first guided document increment: selected-job evaluation, Markdown application packets, and interview plan/practice/debrief with saved review artifacts. Canonical evaluation-to-tracker registration, PDF/ATS export and independent research remain follow-on work.

### Reviewed evaluations and application PDF export

The `record-evaluations-and-export-applications` OpenSpec increment adds Documents actions: **Record reviewed evaluation** → review company/role/URL/optional score → **Save as Evaluated**; and **Review and export PDF** → choose content/job evaluation → **Run quality review** → review exact text/findings → acknowledge → **Save PDF and check notes**. Resume-only export requires one Resume heading. Checks are diagnostic, not fact verification or an ATS guarantee. No application is submitted and no automatic Applied transition exists. PDF/check artifacts appear in the live library; original reviews and master CV remain.

Owner activation helper: `portal/deploy/activate-application-export.py` (qualified release only; `--rollback` restores prior service/env definitions). Automatic backups refuse interrupted registration journals until recovery. These capabilities are staged until owner activation and subsequent live verification.
