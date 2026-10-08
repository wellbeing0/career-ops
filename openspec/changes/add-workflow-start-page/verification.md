# Verification

Seventeen portal tests pass; OpenSpec is strict valid. No mirrored content tests were added for this static copy/layout change.

The staged static release preserves every existing served archive file byte-for-byte except the replaced index, and adds only the home stylesheet. Both prior qualified web builds were reused after comparing 595 runtime source files with the active application-export release; all were unchanged. Updated public Assistant guides have release-bound commit and hash manifests.

Headless browser checks passed at 390×844 and 1280×900: six steps, eight feature explanations, Brad-first workspace links, no horizontal overflow or page errors, system dark/light themes, pointer/hover/pressed feedback, keyboard focus and minimum primary-link touch height. Phone and desktop full-page screenshots were visually reviewed. All eight real authenticated workspace destinations returned HTTP 200.

The staged release `20261008-start-page-01` is sealed with source hashes, both build IDs, the static manifest hash and the browser qualification receipt. Activation swaps the static page and matching Assistant context together, with rollback records for the prior portal pointer and service definitions. No candidate data, login, model or Caddy changes are included.

Owner activation completed successfully using:

```bash
sudo python3 /home/codex-deploy/apps/career-ops-editor/releases/20261008-start-page-01/portal/deploy/activate-start-page.py
```

Live acceptance after owner activation passed: the authenticated public index serves the new workflow page; Brad and Steve workspace, Pipeline and Assistant links return HTTP 200; unauthenticated index returns HTTP 401. Both services use the new release and are active, both backup timers remain active, and the four Assistant guide hashes match the activated release manifest. This acceptance verifies deployed context files and the existing per-turn loading path; no additional model trial was run for this navigation-only deployment.
