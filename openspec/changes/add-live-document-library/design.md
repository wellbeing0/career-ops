# Design

A code-only root helper uses the canonical nested-checkout guard to enumerate selected candidate document areas. Hidden runtime, backups, migrations, credentials, symlinks, nested checkouts and oversized files are excluded. Known credential patterns in text are omitted. Current and archive copies have distinct stable identifiers and source labels. Current text is rendered without executing HTML; original files download as attachments. Archived view/download links stay under the fixed authenticated candidate portal path.

The root-owned activation helper verifies the current static manifest by hash and writes only a candidate-specific archive metadata index into each .hosted directory under the edit lock. It does not migrate or copy candidate content. Subsequent live inventories read VPS files directly, so new generated documents appear on tab opening, focus, thirty-second refresh or manual refresh. A direct `?view=documents` link opens the library.

Only authenticated GET /api/hosted/documents is allowed; arbitrary paths, cross-candidate IDs and writes are rejected. Original current downloads use attachment disposition and nosniff. Binary document previews defer to downloading the original; markdown uses safe rendering and HTML remains source text.

Next AI planning is recorded separately in next-ai-phase.md. No existing Telegram/OpenClaw configuration, provider credentials, paid routes or submission capabilities are changed.

## Navigation and theme follow-up

After owner activation, the portal home still linked View documents to the dated archive. Update those links and candidate navigation to the live Documents tab; retain explicit archive labels and a live-library link on older archive indexes. Apply the workspace neutral light/dark palette through prefers-color-scheme so Steve sees dark on his current device while Brad retains his own device preference. This presentation-only release copies the published VPS snapshot, verifies unchanged original document bytes and switches the existing static symlink without changing Caddy, logins or candidate data.
