#!/usr/bin/env python3
"""Administrator-managed test login; never prints or commits its password."""
import os,pathlib,pwd,secrets,subprocess,sys,re
if os.geteuid()!=0:raise SystemExit('Run with sudo')
auth=pathlib.Path('/etc/caddy/private/careerops-auth.caddy');target=pathlib.Path('/home/codex-deploy/.local/share/career-ops-tests/login.netrc');username='careerops-test'
original=auth.read_text();lines=original.splitlines();filtered=[line for line in lines if not re.match(r'\s*'+username+r'\s',line)]
if sys.argv[1:] == ['--remove']:
 updated='\n'.join(filtered)+'\n'
else:
 if not re.fullmatch(r'\s*basicauth\s*\{[^{}]*\}\s*',original):raise SystemExit('Unrecognized login configuration; no changes made')
 password=secrets.token_urlsafe(32)
 hashed=subprocess.check_output(['caddy','hash-password'],input=password+'\n',text=True).strip()
 updated='\n'.join(filtered);index=updated.rfind('}');updated=updated[:index]+'  '+username+' '+hashed+'\n'+updated[index:]+'\n'
 os.umask(0o077);account=pwd.getpwnam('codex-deploy')
 for directory in [target.parents[2],target.parents[1],target.parent]:
  if not directory.exists():directory.mkdir(mode=0o700);os.chown(directory,account.pw_uid,account.pw_gid)
 os.chown(target.parent,account.pw_uid,account.pw_gid)
 tmp=target.with_suffix('.tmp');tmp.write_text('machine careerops.steveleclair.info\nlogin '+username+'\npassword '+password+'\n');os.chmod(tmp,0o600);os.chown(tmp,account.pw_uid,account.pw_gid);tmp.replace(target)
 del password,hashed
try:
 auth.write_text(updated)
 subprocess.run(['caddy','validate','--config','/etc/caddy/Caddyfile','--adapter','caddyfile'],check=True)
 subprocess.run(['systemctl','reload','caddy'],check=True)
except BaseException:
 auth.write_text(original);subprocess.run(['systemctl','reload','caddy']);target.unlink(missing_ok=True);raise
if sys.argv[1:] == ['--remove']:target.unlink(missing_ok=True)
print('Testing login removed.' if sys.argv[1:] == ['--remove'] else 'Testing login enabled; credential stored privately. Existing shared login retained.')
