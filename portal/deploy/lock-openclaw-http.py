#!/usr/bin/env python3
"""Keep OpenClaw OpenAI-compatible HTTP APIs local; preserve owner dashboard proxy."""
import argparse,pathlib,os,subprocess,datetime,tempfile
RULE='\n\t# Career AI HTTP APIs are server-local; never proxy them publicly.\n\t@career_private_ai path /v1 /v1/*\n\trespond @career_private_ai 404\n'
def restricted_config(text):
 if '@career_private_ai' in text:
  if RULE in text:return text
  raise ValueError('Existing API restriction differs; review required')
 if text.count('openclaw.steveleclair.info {')!=1 or text.count('reverse_proxy 127.0.0.1:18789')!=1:raise ValueError('OpenClaw site changed; review required')
 return text.replace('\n\treverse_proxy 127.0.0.1:18789',RULE+'\n\treverse_proxy 127.0.0.1:18789')
def main():
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
 target=pathlib.Path('/etc/caddy/conf.d/openclaw.steveleclair.info.caddy');before=target.read_text();after=restricted_config(before)
 if a.check:
  with tempfile.TemporaryDirectory(prefix='career-caddy-check-') as d:
   f=pathlib.Path(d)/'Caddyfile';f.write_text(after)
   subprocess.run(['caddy','validate','--config',str(f),'--adapter','caddyfile'],check=True)
  print('Restriction syntax verified; no live change.');return
 if os.geteuid()!=0:raise SystemExit('Run with sudo')
 if before==after:print('Public AI HTTP API is already blocked.');return
 os.umask(0o077);folder=pathlib.Path('/etc/career-ops');folder.mkdir(exist_ok=True)
 backup=folder/('openclaw-public-http-'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')+'.caddy');backup.write_text(before)
 def write(text):
  stat=target.stat();tmp=target.with_name(target.name+'.career-update');tmp.write_text(text);os.chmod(tmp,stat.st_mode&0o777);os.chown(tmp,stat.st_uid,stat.st_gid);os.replace(tmp,target)
 try:
  write(after);subprocess.run(['caddy','validate','--config','/etc/caddy/Caddyfile','--adapter','caddyfile'],check=True);subprocess.run(['systemctl','reload','caddy'],check=True)
 except BaseException:
  write(before);subprocess.run(['systemctl','reload','caddy']);raise SystemExit('Restriction failed; previous OpenClaw site restored.')
 print('Public OpenClaw /v1 API blocked. Career Ops local AI connection retained. Owner dashboard proxy retained. Backup: '+str(backup))
if __name__=='__main__':main()
