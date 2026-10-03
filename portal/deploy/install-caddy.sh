#!/usr/bin/env bash
# Administrator-run once; document publication never changes this configuration.
set -euo pipefail
[[ $(id -u) == 0 ]] || { echo 'Run this installer with sudo.' >&2; exit 1; }
domain=${1:-careerops.steveleclair.info}
[[ "$domain" == careerops.steveleclair.info ]] || { echo 'This reviewed installer is only for careerops.steveleclair.info.' >&2; exit 1; }
base=/home/codex-deploy/apps/career-ops-portal
site=/etc/caddy/conf.d/careerops.steveleclair.info.caddy
auth=/etc/caddy/private/careerops-auth.caddy
[[ -s "$base/current/site/index.html" ]] || { echo 'No verified release staged.' >&2; exit 1; }
python3 "$base/deploy/activate.py" --base "$base" --release "$(basename "$(readlink -f "$base/current")")" >/dev/null
command -v caddy >/dev/null
grep -Fq 'import /etc/caddy/conf.d/*.caddy' /etc/caddy/Caddyfile || { echo 'Expected Caddy conf.d import is absent; no changes made.' >&2; exit 1; }
# Confirm Caddy can traverse and read the staged public tree without widening permissions.
runuser -u caddy -- test -r "$base/current/site/index.html" || { echo 'Caddy cannot read the staged snapshot; no changes made.' >&2; exit 1; }
umask 077
install -d -o root -g caddy -m 0750 /etc/caddy/private
if [[ ! -f "$auth" ]]; then
 read -r -p 'Shared login username [careerops]: ' username </dev/tty
 username=${username:-careerops}
 [[ "$username" =~ ^[a-zA-Z0-9_-]{1,64}$ ]] || { echo 'Use letters, digits, underscore or hyphen for username.' >&2; exit 1; }
 read -r -s -p 'New shared password (at least 8 characters): ' password </dev/tty; echo >/dev/tty
 read -r -s -p 'Repeat password: ' repeat </dev/tty; echo >/dev/tty
 [[ "$password" == "$repeat" && ${#password} -ge 8 ]] || { unset password repeat; echo 'Password mismatch or too short.' >&2; exit 1; }
 hash=$(printf '%s\n' "$password" | caddy hash-password)
 unset password repeat
 printf 'basicauth {\n  %s %s\n}\n' "$username" "$hash" > "$auth"
 unset hash
 chown root:caddy "$auth"; chmod 0640 "$auth"
else
 echo 'Keeping the existing shared login.'
fi
backup=$(mktemp /etc/caddy/private/careerops-config-backup.XXXXXX)
had_previous=0
if [[ -f "$site" ]]; then cp -p "$site" "$backup"; had_previous=1; fi
staged=$(mktemp /etc/caddy/private/careerops-config-new.XXXXXX)
trap 'rm -f "$staged"' EXIT
cat > "$staged" <<EOF
$domain {
  route {
    import $auth
    @writes not method GET HEAD
    respond @writes 405
    header {
      Cache-Control "private, no-store"
      X-Robots-Tag "noindex, nofollow, noarchive"
      X-Content-Type-Options "nosniff"
      Referrer-Policy "no-referrer"
      Content-Security-Policy "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-src 'self'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'"
    }
    root * $base/current/site
    file_server
  }
}
EOF
install -o root -g root -m 0644 "$staged" "$site"
if ! caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile; then
 if [[ "$had_previous" == 1 ]]; then cp -p "$backup" "$site"; else rm -f "$site"; fi
 echo 'Validation failed; previous site configuration restored. Caddy was not reloaded.' >&2
 exit 1
fi
if ! systemctl reload caddy; then
 if [[ "$had_previous" == 1 ]]; then cp -p "$backup" "$site"; else rm -f "$site"; fi
 caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile && systemctl reload caddy
 echo 'Reload failed; previous configuration restored.' >&2
 exit 1
fi
echo "Site configured permanently: https://$domain"
echo 'Shared credentials remain in /etc/caddy/private/careerops-auth.caddy, outside the website.'
echo 'Keep the shared password in your password manager; share it with Brad separately.'
