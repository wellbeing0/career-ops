# Record reviewed evaluations and export application PDFs

Steve authorized implementation on 2026-10-08 of canonical evaluation-to-Applications registration and PDF export with ATS/fact/title checks. Reuse the bounded hosted interface and candidate-local data; no unrestricted OpenClaw tools.

Add a reviewed evaluation action in Documents (also reachable from saved Assistant results). The candidate reviews company, role, posting URL and optional score; explicit save creates a numbered report and an Evaluated tracker row, never Applied. Preserve the original review, archive its verbatim JD, avoid duplicate posting registrations and recover interrupted writes under the existing canonical tracker lock.

Add quality review and PDF export for current Markdown CV/application documents. Support resume-only extraction from a packet and full-document export. Reuse upstream keyword and title checkers with honest unavailable/unmatched results, a conservative number comparison against current primary files and direct statements captured with the original draft, and an explicit human review acknowledgment. No fact or keyword injection. Save versioned PDF and check notes into Documents. Render escaped text locally with network and JavaScript disabled; no browser-selected URLs.

Stage and qualify both candidate builds, document results, commit/push without PR, and provide the existing owner sudo activation handoff. Root activation remains owner-run. No candidate test documents are written to production just to qualify the release.
