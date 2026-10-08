#!/usr/bin/env python3
"""Activate only the qualified code release; retain private, reversible unit/env changes."""
import argparse,hashlib,json,os,pathlib,re,subprocess,time,urllib.request,urllib.error
import sys
sys.path.insert(0,str(pathlib.Path(__file__).parent))
from activate import activate,verify
portal_base=pathlib.Path('/home/codex-deploy/apps/career-ops-portal')
portal_release='20261008-compact-guide-01'
portal_journal=pathlib.Path('/etc/career-ops/compact-guide-portal-20261008-01.json')
def restore_portal():
 if portal_journal.exists():
  previous=json.loads(portal_journal.read_text())['previous']
  if not re.fullmatch(r'releases/[a-z0-9-]{1,80}',previous):raise SystemExit('Unexpected previous portal release')
  activate(portal_base,previous.split('/')[1])
p=argparse.ArgumentParser();p.add_argument('--rollback',action='store_true');a=p.parse_args()
if os.geteuid()!=0:raise SystemExit('Run with sudo')
release=pathlib.Path('/home/codex-deploy/apps/career-ops-editor/releases/20261008-compact-guide-01')
journal=pathlib.Path('/etc/career-ops/compact-guide-activation-20261008-01.json')
if a.rollback:
 restore_portal()
 records=json.loads(journal.read_text())
 for r in records:pathlib.Path(r['file']).write_text(r['before'])
 subprocess.run(['systemctl','daemon-reload'],check=True)
 subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
 print('Previous editor and backup definitions restored. Candidate files and search results retained.')
 raise SystemExit(0)
if not (release/'QUALIFIED').is_file():raise SystemExit('Qualified start-page release missing')
qualified=json.loads((release/'QUALIFIED').read_text())
if qualified.get('format')!='career-assistant-qualified-v1':raise SystemExit('Invalid qualification receipt')
for name,digest in qualified['source_sha256'].items():
 file=release/name
 if not file.resolve().is_relative_to(release.resolve()) or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:raise SystemExit('Qualified source changed; activate refused')
knowledge=json.loads((release/'portal/knowledge/manifest.json').read_text())
if knowledge.get('release')!=release.name or qualified.get('sourceCommit')!=knowledge.get('sourceCommit'):raise SystemExit('Project knowledge release mismatch')
for name,digest in knowledge['sha256'].items():
 if name not in ['project-overview.md','workspace-guide.md','search-pipeline-guide.md','assistant-capabilities.md'] or hashlib.sha256((release/'portal/knowledge'/name).read_bytes()).hexdigest()!=digest:raise SystemExit('Project knowledge changed')
for candidate in ['brad','steve']:
 if (release/'web'/('.next-'+candidate)/'BUILD_ID').read_text().strip()!=qualified['build_ids'][candidate]:raise SystemExit('Qualified build changed; activate refused')
static=portal_base/'releases'/portal_release
manifest=verify(static)
if hashlib.sha256((static/'manifest.json').read_bytes()).hexdigest()!=qualified['portal_manifest_sha256']:raise SystemExit('Qualified start page changed')
current=os.readlink(portal_base/'current')
if current not in [manifest['home_source'],'releases/'+portal_release]:raise SystemExit('Current portal changed; review before activation')
records=[]
for candidate in ['brad','steve']:
 env=pathlib.Path('/etc/career-ops/'+candidate+'.env');before=env.read_text()
 if 'CAREER_OPS_ROOT=/var/lib/career-ops/'+candidate+'\n' not in before:raise SystemExit('Unexpected candidate data root; no update made')
 after,n=re.subn(r'^CAREER_OPS_CODE_ROOT=.*$','CAREER_OPS_CODE_ROOT='+str(release),before,flags=re.M);assert n==1
 records.append({'file':str(env),'before':before,'after':after})
 for suffix in ['.service','-backup.service']:
  unit=pathlib.Path('/etc/systemd/system/careerops-'+candidate+suffix);before=unit.read_text()
  if suffix=='.service':after,n=re.subn(r'^WorkingDirectory=.*$','WorkingDirectory='+str(release/'web'),before,flags=re.M)
  else:after,n=re.subn(r'(?m)^ExecStart=/usr/bin/python3 \S+/portal/deploy/candidate-backup.py ', 'ExecStart=/usr/bin/python3 '+str(release/'portal/deploy/candidate-backup.py')+' ',before)
  assert n==1
  records.append({'file':str(unit),'before':before,'after':after})
if journal.exists():
 existing=json.loads(journal.read_text())
 if all(pathlib.Path(r['file']).read_text()==r['after'] for r in existing):
  subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
  activate(portal_base,portal_release)
  print('Start page and matching Assistant context are already active.');raise SystemExit(0)
 raise SystemExit('Activation journal exists with different state; review or roll back before retrying')
os.umask(0o077)
if portal_journal.exists():raise SystemExit('Portal activation journal already exists; review before retrying')
with portal_journal.open('x') as out:json.dump({'previous':current},out)
with journal.open('x') as out:json.dump(records,out)
try:
 for r in records:pathlib.Path(r['file']).write_text(r['after'])
 subprocess.run(['systemctl','daemon-reload'],check=True)
 subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
 for candidate,port in [('brad',3921),('steve',3922)]:
  subprocess.run(['systemctl','is-active','--quiet','careerops-'+candidate],check=True)
  for attempt in range(20):
   try:urllib.request.urlopen(f'http://127.0.0.1:{port}/{candidate}/workspace/api/hosted/search',timeout=2)
   except urllib.error.HTTPError as error:
    if error.code==401:break
   except OSError:pass
   time.sleep(1)
  else:raise RuntimeError('Search service startup did not qualify')
 activate(portal_base,portal_release)
except BaseException:
 restore_portal()
 for r in records:pathlib.Path(r['file']).write_text(r['before'])
 subprocess.run(['systemctl','daemon-reload']);subprocess.run(['systemctl','restart','careerops-brad','careerops-steve']);journal.unlink();portal_journal.unlink()
 raise
print('Workflow start page and matching Assistant guides activated for Brad and Steve. Shared login, archives, authoritative data, model configuration and backup timers preserved.')
