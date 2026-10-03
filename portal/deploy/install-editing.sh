#!/usr/bin/env bash
# Reviewed phase-2A administrator cutover; preserves the existing shared login.
set -euo pipefail
[[ $(id -u) == 0 ]] || { echo 'Run with sudo.' >&2; exit 1; }
base=/home/codex-deploy/apps/career-ops-editor
release=$(readlink -f "$base/staged")
[[ "$release" == "$base/releases/"* && -f "$release/QUALIFIED" ]] || { echo 'Qualified release missing.' >&2; exit 1; }
[[ -f /etc/caddy/private/careerops-auth.caddy ]] || { echo 'Existing login required.' >&2; exit 1; }
umask 077
install -d -m 0755 /var/lib/career-ops
install -d -m 0700 /etc/career-ops
site=/etc/caddy/conf.d/careerops.steveleclair.info.caddy
backup=/etc/career-ops/viewing-caddy-backup
[[ -f "$backup" ]] || cp -p "$site" "$backup"
for candidate in brad steve; do
 user=careerops-$candidate
 id "$user" >/dev/null 2>&1 || useradd --system --user-group --no-create-home --shell /usr/sbin/nologin "$user"
 root=/var/lib/career-ops/$candidate
 if [[ ! -e "$root" ]]; then
  install -d -o "$user" -g "$user" -m 0700 "$root"
  python3 "$release/portal/deploy/migrate-candidate.py" "$base/incoming/$candidate" "$root"
  chown -R "$user:$user" "$root"
 fi
 runuser -u "$user" -- test -r "$root/cv.md"
 if [[ ! -e /etc/career-ops/$candidate.env ]]; then
 token=$(openssl rand -hex 32)
 port=3921; [[ "$candidate" == steve ]] && port=3922
 cat > /etc/career-ops/$candidate.env <<EOF
NEXT_TELEMETRY_DISABLED=1
CAREER_OPS_HOSTED=1
NEXT_PUBLIC_HOSTED_MODE=1
NEXT_PUBLIC_HOSTED_BASE=/$candidate/workspace
BUILD_DIST=.next-$candidate
CAREER_OPS_CANDIDATE=$candidate
CAREER_OPS_ROOT=$root
CAREER_OPS_CODE_ROOT=$release
CAREER_OPS_GATEWAY_TOKEN=$token
CAREER_OPS_WEB_ALLOWED_HOSTS=careerops.steveleclair.info
HOME=$root
EOF
 chmod 0600 /etc/career-ops/$candidate.env
 cat > /etc/caddy/private/careerops-$candidate-gateway.caddy <<EOF
reverse_proxy 127.0.0.1:$port {
 header_up X-Career-Gateway $token
}
EOF
 unset token
 chown root:caddy /etc/caddy/private/careerops-$candidate-gateway.caddy
 chmod 0640 /etc/caddy/private/careerops-$candidate-gateway.caddy
 else
  [[ -s /etc/caddy/private/careerops-$candidate-gateway.caddy ]] || { echo "Existing runtime is missing its gateway configuration." >&2; exit 1; }
  port=3921; [[ "$candidate" == steve ]] && port=3922
 fi
 cat > /etc/systemd/system/careerops-$candidate.service <<EOF
[Unit]
Description=Career Ops $candidate editing workspace
After=network.target
[Service]
User=$user
Group=$user
WorkingDirectory=$release/web
EnvironmentFile=/etc/career-ops/$candidate.env
ExecStart=/usr/bin/node node_modules/next/dist/bin/next start --hostname 127.0.0.1 --port $port
Restart=on-failure
RestartSec=3
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=$root
MemoryMax=768M
[Install]
WantedBy=multi-user.target
EOF
 runuser -u "$user" -- python3 "$release/portal/deploy/candidate-backup.py" "$root" "$root/.hosted/backups" --drill
 # Backups are prepared but their timer remains disabled until production acceptance.
 cat > /etc/systemd/system/careerops-$candidate-backup.service <<EOF
[Unit]
Description=Private Career Ops $candidate snapshot
[Service]
Type=oneshot
User=$user
Group=$user
UMask=0077
ExecStart=/usr/bin/python3 $release/portal/deploy/candidate-backup.py $root $root/.hosted/backups
EOF
 cat > /etc/systemd/system/careerops-$candidate-backup.timer <<EOF
[Unit]
Description=Daily Career Ops $candidate snapshot (enable after acceptance)
[Timer]
OnCalendar=daily
Persistent=true
RandomizedDelaySec=15m
[Install]
WantedBy=timers.target
EOF
done
systemctl daemon-reload
systemctl start careerops-brad careerops-steve
for port in 3921 3922; do
 ready=0
 for attempt in {1..20}; do
  code=$(curl --max-time 2 -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port/" || true)
  [[ "$code" == 401 || "$code" == 404 || "$code" == 403 ]] && { ready=1; break; }
  sleep 1
 done
 [[ "$ready" == 1 ]] || { echo 'Workspace failed startup; Caddy unchanged.' >&2; exit 1; }
done
cat > "$site" <<EOF
careerops.steveleclair.info {
 route {
  import /etc/caddy/private/careerops-auth.caddy
  header {
   Cache-Control "private, no-store"
   X-Robots-Tag "noindex, nofollow, noarchive"
   X-Content-Type-Options "nosniff"
   Referrer-Policy "no-referrer"
  }
  @brad path /brad/workspace /brad/workspace/*
  handle @brad { import /etc/caddy/private/careerops-brad-gateway.caddy }
  @steve path /steve/workspace /steve/workspace/*
  handle @steve { import /etc/caddy/private/careerops-steve-gateway.caddy }
  handle {
   @writes not method GET HEAD
   respond @writes 405
   header Content-Security-Policy "default-src 'none'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-src 'self'; script-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'self'"
   root * /home/codex-deploy/apps/career-ops-portal/current/site
   file_server
  }
 }
}
EOF
# Expand handle blocks: Caddy 2.6 requires imports on their own lines.
python3 - "$site" <<'PY'
import sys
p=sys.argv[1];s=open(p).read();s=s.replace('handle @brad { import /etc/caddy/private/careerops-brad-gateway.caddy }','handle @brad {\n   import /etc/caddy/private/careerops-brad-gateway.caddy\n  }').replace('handle @steve { import /etc/caddy/private/careerops-steve-gateway.caddy }','handle @steve {\n   import /etc/caddy/private/careerops-steve-gateway.caddy\n  }');open(p,'w').write(s)
PY
if ! caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile || ! systemctl reload caddy; then
 cp -p "$backup" "$site"
 systemctl reload caddy
 echo 'Viewing configuration restored. Candidate data remains preserved.' >&2; exit 1
fi
systemctl enable careerops-brad careerops-steve
printf 'VPS authority active. Verify both logged-in workspaces before enabling backup timers.\n'
