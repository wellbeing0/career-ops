#!/usr/bin/env python3
"""Approved global Skill Workshop change; native validation and private rollback."""
import copy,datetime,json,os,pathlib,subprocess,time
RUNTIME='/home/steve/.npm-global/bin/openclaw'
VERSION='OpenClaw 2026.9.8 (fc23bc8)'
PREFIX='skill-collection-review:'
def propose_config(original):
 result=copy.deepcopy(original)
 result.setdefault('skills',{}).setdefault('workshop',{}).setdefault('autonomous',{})['mode']='propose'
 return result

def command(args,env=None):
 return subprocess.run(args,capture_output=True,text=True,env=env,timeout=35)

def jobs():
 p=command([RUNTIME,'cron','list','--all','--json','--timeout','10000'])
 if p.returncode:raise RuntimeError('Gateway control inspection unavailable')
 return json.loads(p.stdout).get('jobs',[])

def main():
 if pathlib.Path.home()!=pathlib.Path('/home/steve'):raise SystemExit('Run as steve without sudo')
 if command([RUNTIME,'--version']).stdout.strip()!=VERSION:raise SystemExit('Unqualified installed runtime')
 os.umask(0o077)
 path=pathlib.Path('/home/steve/.openclaw/openclaw.json');before=path.read_text();original=json.loads(before);proposed=propose_config(original)
 validation=path.with_name('workshop-propose-validation.json');validation.write_text(json.dumps(proposed))
 try:
  p=command([RUNTIME,'config','validate'],{**os.environ,'OPENCLAW_CONFIG_PATH':str(validation)})
  if p.returncode:raise SystemExit('Native schema rejected proposed settings; no change made')
 finally:validation.unlink(missing_ok=True)
 oldjobs=jobs();review=[j for j in oldjobs if j.get('declarationKey','').startswith(PREFIX)]
 if not any(j.get('agentId')=='career-brad' for j in review):raise SystemExit('Brad review definition missing; inspect before applying')
 backup=pathlib.Path('/home/steve/.openclaw-career-backups')/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ-workshop')
 backup.mkdir(parents=True,mode=0o700);(backup/'openclaw.json').write_text(before);(backup/'jobs.json').write_text(json.dumps(oldjobs))
 after=json.dumps(proposed,indent=2)+'\n'
 def write(value):
  mode=path.stat().st_mode&0o777;tmp=path.with_name('openclaw.json.workshop-propose');tmp.write_text(value);os.chmod(tmp,mode);os.replace(tmp,path)
 if path.read_text()!=before:raise SystemExit('Concurrent configuration change; no change made')
 write(after)
 try:
  deadline=time.monotonic()+180
  while time.monotonic()<deadline:
   try:
    current=jobs();byid={j['id']:j for j in current}
    retained=all(j['id'] in byid and byid[j['id']].get('enabled') is False for j in review)
    unaffected=all(byid.get(j['id'],{}).get('enabled')==j.get('enabled') for j in oldjobs if not j.get('declarationKey','').startswith(PREFIX))
    if retained and unaffected:break
   except RuntimeError:pass
   time.sleep(3)
  else:raise RuntimeError('Monitor reconciliation not verified within startup grace')
  if json.loads(path.read_text())!=proposed:raise RuntimeError('Configuration changed during verification')
 except BaseException:
  if path.read_text()==after:write(before)
  raise SystemExit('Workshop verification failed; scoped rollback attempted. Private backup: '+str(backup))
 print(json.dumps({'workshopMode':'propose','reviewJobsDisabled':len(review),'definitionsRetained':True,'unrelatedSchedules':'preserved','allOtherConfiguration':'preserved','backup':str(backup)}))
if __name__=='__main__':main()
