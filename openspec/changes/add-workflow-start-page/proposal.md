# A simple re-entry page for Career Ops

Steve requested a concise index page explaining the intended job-search path and core features, especially for Brad returning without development context. Implement an authenticated, responsive static start page with Brad-first workspace choices, Search/Pipeline/Assistant shortcuts, six numbered workflow steps and one-line feature explanations. Avoid live counts, dated archive framing, a giant help center or a new onboarding requirement. Preserve human review and manual submission.

Ship updated OpenClaw context with this deployment. Stage a static release preserving every existing archived file, and a matching system-code release with refreshed guide hashes. Reuse the unchanged qualified web builds only after byte-for-byte source comparison; no web code changes are needed. Owner sudo activation switches the guides and start page together with rollback. No Caddy, login, candidate data, model or backup-policy changes.
