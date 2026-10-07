#!/usr/bin/env python3
"""Owner-scoped 2026.9.8 career settings repair; no root or candidate file access."""
import argparse,copy,json,pathlib,subprocess,os,datetime,time,urllib.request,urllib.error
VERSION='OpenClaw 2026.9.8 (fc23bc8)'
RUNTIME='/home/steve/.npm-global/bin/openclaw'
def brad_config(original):
 c=copy.deepcopy(original);entries=c.get('agents',{}).get('entries',{})
 if set(entries)!={'main','career-brad','career-steve'}:raise ValueError('Agent fleet changed; review required')
 brad=entries['career-brad']
 if brad.get('tools',{}).get('deny')!=['*'] or brad.get('tools',{}).get('elevated',{}).get('enabled') is not False or brad.get('memory',{}).get('search',{}).get('enabled') is not False or brad.get('heartbeat',{}).get('every')!='0m':raise ValueError('Career restrictions changed; review required')
 if not isinstance(brad.get('model'),dict) or not brad['model'].get('primary','').startswith('openai/'):raise ValueError('Model configuration changed; review required')
 brad['model']['primary']='openai/gpt-6.1-sol';brad['thinkingDefault']='medium';return c
def command(args,env=None):
 return subprocess.run(args,env=env,capture_output=True,text=True,timeout=90)
def main():
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
 if pathlib.Path.home()!=pathlib.Path('/home/steve'):raise SystemExit('Run as the OpenClaw owner steve, without sudo')
 if command([RUNTIME,'--version']).stdout.strip()!=VERSION:raise SystemExit('Runtime changed; qualify it before applying')
 config=pathlib.Path('/home/steve/.openclaw/openclaw.json');before=config.read_text();after=json.dumps(brad_config(json.loads(before)),indent=2)+'\n'
 os.umask(0o077);validation=config.with_name('career-runtime-validation-20261007.json');validation.write_text(after)
 try:
  valid=command([RUNTIME,'config','validate'],{**os.environ,'OPENCLAW_CONFIG_PATH':str(validation)})
  if valid.returncode:raise SystemExit('Installed schema rejected proposed settings; no change made')
 finally:validation.unlink(missing_ok=True)
 for attempt in range(6):
  jobs=command([RUNTIME,'cron','list','--all','--json','--timeout','10000'])
  if not jobs.returncode:break
  time.sleep(2)
 else:raise SystemExit('Scheduled-job inspection failed; no change made')
 matching=[j for j in json.loads(jobs.stdout).get('jobs',[]) if j.get('agentId')=='career-brad' and j.get('name')=='skill-collection-review-career-brad']
 if len(matching)>1:raise SystemExit('Multiple matching maintenance jobs; review required')
 if not a.apply:print('Installed schema accepts Brad GPT-6.1 Sol / medium. Maintenance job identified. No change made.');return
 if config.read_text()!=before:raise SystemExit('Configuration changed during validation; retry')
 backup=pathlib.Path('/home/steve/.openclaw-career-backups')/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');backup.mkdir(parents=True,mode=0o700)
 (backup/'openclaw.json').write_text(before);(backup/'maintenance-job.json').write_text(json.dumps(matching))
 def write(text):
  stat=config.stat();tmp=config.with_name('openclaw.json.career-upgrade');tmp.write_text(text);os.chmod(tmp,stat.st_mode&0o777);os.replace(tmp,config)
 changed=False
 maintenance="absent" if not matching else "already-disabled"
 try:
  if matching and matching[0].get('enabled'):
   result=command([RUNTIME,'cron','disable',matching[0]['id'],'--timeout','10000'])
   if result.returncode:
    if 'system-owned monitor jobs cannot be edited by cron clients' not in result.stderr:raise RuntimeError('Maintenance job could not be paused')
    maintenance='system-owned: global owner decision required'
   else:maintenance='paused'
  write(after);changed=True
  if command(['systemctl','--user','restart','openclaw-gateway.service']).returncode:raise RuntimeError('Restart failed')
  for attempt in range(180):
   try:urllib.request.urlopen('http://127.0.0.1:18789/v1/models',timeout=2)
   except urllib.error.HTTPError as e:
    if e.code==401:break
   except OSError:pass
   time.sleep(1)
  else:raise RuntimeError('Gateway did not start')
  for attempt in range(6):
   check=command([RUNTIME,'cron','list','--all','--json','--timeout','10000'])
   if not check.returncode:break
   time.sleep(2)
  else:raise RuntimeError('Gateway control verification failed after startup grace')
  if maintenance=='paused' and any(j.get('enabled') for j in json.loads(check.stdout).get('jobs',[]) if j.get('id') in {x['id'] for x in matching}):raise RuntimeError('Maintenance job still enabled')
 except BaseException as error:
  if config.read_text()!=after and config.read_text()!=before:raise SystemExit('Configuration changed concurrently; private backup retained for review: '+str(backup))
  if changed:
   write(before);command(['systemctl','--user','restart','openclaw-gateway.service'])
  if maintenance=='paused':command([RUNTIME,'cron','enable',matching[0]['id'],'--timeout','10000'])
  raise SystemExit('Upgrade failed ('+(str(error) if isinstance(error,RuntimeError) else type(error).__name__)+'); previous settings restored. Private backup: '+str(backup))
 print(json.dumps({'version':VERSION,'bradModel':'openai/gpt-6.1-sol','bradThinking':'medium','maintenance':maintenance,'steveModel':'preserved','privateBackup':str(backup)}))
if __name__=='__main__':main()
