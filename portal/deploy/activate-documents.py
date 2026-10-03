#!/usr/bin/env python3
"""Activate only the qualified code release; retain private, reversible unit/env changes."""
import argparse,hashlib,json,os,pathlib,re,subprocess,time,urllib.request,urllib.error
p=argparse.ArgumentParser();p.add_argument('--rollback',action='store_true');a=p.parse_args()
if os.geteuid()!=0:raise SystemExit('Run with sudo')
release=pathlib.Path('/home/codex-deploy/apps/career-ops-editor/releases/20261003-documents-01')
journal=pathlib.Path('/etc/career-ops/documents-activation-20261003-01.json')
if a.rollback:
 records=json.loads(journal.read_text())
 for r in records:pathlib.Path(r['file']).write_text(r['before'])
 subprocess.run(['systemctl','daemon-reload'],check=True)
 subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
 print('Previous editor and backup definitions restored. Candidate files and search results retained.')
 raise SystemExit(0)
if not (release/'QUALIFIED').is_file():raise SystemExit('Qualified Documents release missing')
qualified=json.loads((release/'QUALIFIED').read_text())
if qualified.get('format')!='career-search-qualified-v1':raise SystemExit('Invalid qualification receipt')
for name,digest in qualified['source_sha256'].items():
 file=release/name
 if not file.resolve().is_relative_to(release.resolve()) or hashlib.sha256(file.read_bytes()).hexdigest()!=digest:raise SystemExit('Qualified source changed; activate refused')
for candidate in ['brad','steve']:
 if (release/'web'/('.next-'+candidate)/'BUILD_ID').read_text().strip()!=qualified['build_ids'][candidate]:raise SystemExit('Qualified build changed; activate refused')
def index_archive():
 subprocess.run(['/usr/bin/python3',str(release/'portal/deploy/index-document-archive.py')],check=True)
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
  index_archive();print('Documents release is already active.');raise SystemExit(0)
 raise SystemExit('Activation journal exists with different state; review or roll back before retrying')
os.umask(0o077)
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
except BaseException:
 for r in records:pathlib.Path(r['file']).write_text(r['before'])
 subprocess.run(['systemctl','daemon-reload']);subprocess.run(['systemctl','restart','careerops-brad','careerops-steve']);journal.unlink()
 raise
index_archive()
print('Live document library activated for Brad and Steve. Shared login, authoritative data, history and enabled backup timers preserved.')
