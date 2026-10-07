#!/usr/bin/env python3
"""Owner activation of qualified assistant code and bounded OpenClaw agents; reversible private journal."""
import argparse,pathlib,os,json,hashlib,subprocess,pwd,re,time,urllib.request,urllib.error,importlib.util
p=argparse.ArgumentParser();p.add_argument('--rollback',action='store_true');p.add_argument('--release',default='20261003-assistant-02');a=p.parse_args()
if not re.fullmatch(r'[a-z0-9-]{1,80}',a.release):raise SystemExit('Invalid release identifier')
if os.geteuid()!=0:raise SystemExit('Run with sudo')
os.umask(0o077)
release=pathlib.Path('/home/codex-deploy/apps/career-ops-editor/releases')/a.release;journal=pathlib.Path('/etc/career-ops')/('assistant-activation-'+a.release+'.json');
if a.release=='20261003-assistant-02':journal=pathlib.Path('/etc/career-ops/assistant-activation-20261003-02.json')
owner=pwd.getpwnam('steve');configfile=pathlib.Path('/home/steve/.openclaw/openclaw.json')
def user_command(args):return ['runuser','-u','steve','--','env','HOME=/home/steve','XDG_RUNTIME_DIR=/run/user/'+str(owner.pw_uid),'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/'+str(owner.pw_uid)+'/bus',*args]
def restart():
 subprocess.run(user_command(['systemctl','--user','restart','openclaw-gateway.service']),check=True)
 subprocess.run(['systemctl','daemon-reload'],check=True);subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
def write(file,text):
 file=pathlib.Path(file);temp=file.with_name(file.name+'.careerops-update');temp.write_text(text);temp.chmod(file.stat().st_mode&0o777);os.chown(temp,file.stat().st_uid,file.stat().st_gid);os.replace(temp,file)
if a.rollback:
 records=json.loads(journal.read_text())['records']
 if any(pathlib.Path(item['file']).read_text()!=item['after'] for item in records):raise SystemExit('Configuration changed after activation; review before rollback to preserve later edits')
 for item in records:write(item['file'],item['before'])
 restart();print('Assistant disabled and previous code/OpenClaw configuration restored. Candidate documents and conversations retained.');raise SystemExit(0)
q=json.loads((release/'QUALIFIED').read_text())
if q.get('format')!='career-assistant-qualified-v1':raise SystemExit('Assistant qualification missing')
for name,digest in q['source_sha256'].items():
 f=release/name
 if not f.resolve().is_relative_to(release.resolve()) or hashlib.sha256(f.read_bytes()).hexdigest()!=digest:raise SystemExit('Qualified source changed; activation refused')
for c in ['brad','steve']:
 if (release/'web'/('.next-'+c)/'BUILD_ID').read_text().strip()!=q['build_ids'][c]:raise SystemExit('Qualified build changed')
version=subprocess.check_output(user_command(['/home/steve/.npm-global/bin/openclaw','--version']),text=True).strip()
if version!=q.get('qualifiedOpenClawVersion','OpenClaw 2026.9.3 (1391f7c)'):raise SystemExit('OpenClaw version changed; qualify the installed version before activation')
if journal.exists():
 old=json.loads(journal.read_text())
 if all(pathlib.Path(x['file']).read_text()==x['after'] for x in old['records']):print('Assistant release is already active.');raise SystemExit(0)
 raise SystemExit('Activation journal exists with different state; review or rollback before retrying')
original=configfile.read_text();config=json.loads(original)
if config.get('gateway',{}).get('bind')!='loopback' or config.get('gateway',{}).get('port')!=18789:raise SystemExit('Gateway transport changed; review required')
# Resolve the existing store reference as its owner through the pinned native resolver.
# stdout is a private pipe captured in memory; never print subprocess diagnostics.
resolved=subprocess.run(user_command(['node',str(release/'portal/deploy/resolve-gateway-token.mjs')]),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
if resolved.returncode:raise SystemExit('Existing gateway credential could not be resolved securely; no activation made.')
token=resolved.stdout
if not re.fullmatch(r'[A-Za-z0-9_.:-]{20,512}',token):raise SystemExit('Gateway credential format is unsupported; no activation made.')
spec=importlib.util.spec_from_file_location('career',release/'portal/deploy/career-agent-config.py');transform=importlib.util.module_from_spec(spec);spec.loader.exec_module(transform)
workspace='/home/steve/.openclaw-career-workspaces';updated=transform.career_config(config,workspace)
for c in ['brad','steve']:
 d=pathlib.Path(workspace)/c;d.mkdir(parents=True,exist_ok=True,mode=0o700);os.chown(d,owner.pw_uid,owner.pw_gid)
os.chown(pathlib.Path(workspace),owner.pw_uid,owner.pw_gid);pathlib.Path(workspace).chmod(0o700)
validation=configfile.with_name('careerops-assistant-validation.json');validation.write_text(json.dumps(updated,indent=2));validation.chmod(0o600);os.chown(validation,owner.pw_uid,owner.pw_gid)
try:
 check=subprocess.run(user_command(['env','OPENCLAW_CONFIG_PATH='+str(validation),'/home/steve/.npm-global/bin/openclaw','config','validate']),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if check.returncode:raise SystemExit('Installed OpenClaw rejected the staged career configuration. Raw config diagnostics withheld; no activation made.')
finally:validation.unlink(missing_ok=True)
records=[{'file':str(configfile),'before':original,'after':json.dumps(updated,indent=2)+'\n'}]
for c in ['brad','steve']:
 env=pathlib.Path('/etc/career-ops/'+c+'.env');before=env.read_text()
 if 'CAREER_OPS_ROOT=/var/lib/career-ops/'+c+'\n' not in before:raise SystemExit('Candidate data root changed')
 after,n=re.subn(r'^CAREER_OPS_CODE_ROOT=.*$','CAREER_OPS_CODE_ROOT='+str(release),before,flags=re.M);assert n==1
 after='\n'.join(line for line in after.splitlines() if not line.startswith(('CAREER_OPS_ASSISTANT_ENABLED=','CAREER_OPS_AI_URL=','CAREER_OPS_AI_TOKEN=')))+'\nCAREER_OPS_ASSISTANT_ENABLED=1\nCAREER_OPS_AI_URL=http://127.0.0.1:18789/v1/chat/completions\nCAREER_OPS_AI_TOKEN='+token+'\n'
 records.append({'file':str(env),'before':before,'after':after})
 for suffix in ['.service','-backup.service']:
  unit=pathlib.Path('/etc/systemd/system/careerops-'+c+suffix);before=unit.read_text()
  if suffix=='.service':after,n=re.subn(r'^WorkingDirectory=.*$','WorkingDirectory='+str(release/'web'),before,flags=re.M)
  else:after,n=re.subn(r'(?m)^ExecStart=/usr/bin/python3 \S+/portal/deploy/candidate-backup.py ', 'ExecStart=/usr/bin/python3 '+str(release/'portal/deploy/candidate-backup.py')+' ',before)
  assert n==1;records.append({'file':str(unit),'before':before,'after':after})
with journal.open('x') as out:json.dump({'records':records,'version':version,'paidFallback':True,'spendingControl':'OpenRouter account limit'},out)
try:
 for item in records:write(item['file'],item['after'])
 restart()
 for c,port in [('brad',3921),('steve',3922)]:
  for attempt in range(30):
   try:urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/'+c+'/workspace/api/hosted/assistant',timeout=2)
   except urllib.error.HTTPError as e:
    if e.code==401:break
   except OSError:pass
   time.sleep(1)
  else:raise RuntimeError('Assistant web service did not start')
 for attempt in range(30):
  try:
   request=urllib.request.Request('http://127.0.0.1:18789/v1/models',headers={'Authorization':'Bearer '+token})
   with urllib.request.urlopen(request,timeout=3) as response:models=json.load(response)
   ids={x['id'] for x in models.get('data',[])}
   if {'openclaw/career-brad','openclaw/career-steve'}.issubset(ids):break
  except OSError:pass
  time.sleep(1)
 else:raise RuntimeError('Career agent routing did not start')
except BaseException:
 for item in records:write(item['file'],item['before'])
 restart();journal.unlink(missing_ok=True);raise SystemExit('Activation did not qualify; previous configuration/code restored. Credentials and raw diagnostics withheld.')
print('Career Assistant activated for Brad and Steve using OpenAI subscription access. OpenRouter fallback uses the existing chain and account-level spending limit. Personal Telegram routing, documents, history and backups preserved. No model trial was run by activation.')
