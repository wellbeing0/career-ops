# Phase 1 verification and administrator handoff

Verified on October 2, 2026. Implementation and staging are complete; public live acceptance remains pending the owner's administrator action.

## Evidence

- `openspec validate add-private-career-portal --strict`: pass.
- OpenSpec autonomy check: no generated skill copies were installed; existing career-ops instructions preserved.
- `python3 -m unittest discover -s portal/tests -v`: seven tests pass (candidate separation, byte-preserved sources, excluded archives, escaping, secret-content detection, symlink escapes, manifest integrity, immutable output and activation refusal).
- Actual private snapshot: 42 selected documents for Steve, 46 for Brad; 180 served files including previews/catalogs/assets. Private hash manifest is outside the served tree and mode 0600 on VPS.
- Browser checks: desktop homepage, both candidate catalogs, all catalog links, sample-resume preview and 390-pixel mobile layout; no mobile horizontal overflow. Screenshots visually reviewed.
- VPS release `20261002-phase1-01` staged and hash-verified; `current` activated. No other site or permanent Caddy configuration was changed.
- Temporary Caddy 2.6.2 loopback test generated from the actual installer template: complete config validates; every one of 180 served files returns 401 unauthenticated; valid candidate navigation/downloads pass; authenticated POST returns 405; manifest, credentials and excluded archive paths return 404. Disposable test credentials are not the production login.
- Caddy service is enabled for reboot. Deployment-account home permits traversal; staged index readable; private manifest is not world-readable.
- Shell syntax check and repository diff whitespace check pass. Existing unrelated `.gitignore` change preserved; no commit or push.

## Owner action

From a sudo-capable administrator terminal on the VPS:

```sh
sudo bash /home/codex-deploy/apps/career-ops-portal/deploy/install-caddy.sh careerops.steveleclair.info
```

First run asks for a shared username (default `careerops`) and a new password with at least 8 characters, repeated for confirmation. It stores only the Caddy hash in `/etc/caddy/private/careerops-auth.caddy` under root ownership and restrictive access. Save/share the password through the owner's password manager; no password belongs in chat, repository or published documents.

The site block will persist in `/etc/caddy/conf.d/careerops.steveleclair.info.caddy`; TLS is managed by Caddy. The installer checks the current snapshot, validates the full configuration and reloads, preserving unrelated sites and restoring its prior site file on failure. Running it again retains the login.

## Remaining acceptance

After the owner runs the command, verify actual public HTTPS and 401 challenges on `/`, `/brad/`, `/steve/` and representative downloads. Owner tests the new shared login in a browser and confirms both workspaces and downloads. Confirm authenticated mutation denial and private-path refusal on the live domain. Record these checks and then mark task 3.5 complete; do not archive the change before live acceptance.

## Updating documents

Build a new uniquely named snapshot from the same explicit candidate roots, transfer and verify it, then activate the new symlink. Keep the previous snapshot for rollback. No permanent sudo grant, password change or Caddy edit is needed for routine document updates.

## Live follow-up after owner setup — October 2, 2026

Owner reported administrator installation complete. Public HTTPS requests succeeded with certificate validation and returned 401 plus a Basic authentication challenge for the homepage, both candidate directories, Brad's original PDF, Steve's master CV download and the manifest path. Caddy is active; the site configuration exists as root-owned 0644. The private credential directory is root:caddy 0750; the deployment account cannot inspect its contained credential file, as intended. Its exact file mode was not independently inspected after installation.

Authenticated public navigation/downloads and mutation/private-path checks remain pending owner browser verification. They passed the prior isolated Caddy integration test, but that does not replace live authenticated acceptance. No production credentials were read or requested. Task 3.5 remains open for these remaining checks.
