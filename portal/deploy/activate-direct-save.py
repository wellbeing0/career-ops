#!/usr/bin/env python3
"""Administrator code-only update. Does not import, restore or rewrite candidate data."""
import os,pathlib,re,subprocess,time,urllib.request,urllib.error
if os.geteuid()!=0:raise SystemExit('Run with sudo')
release=pathlib.Path('/home/codex-deploy/apps/career-ops-editor/releases/20261003-direct-save-01')
if not (release/'QUALIFIED').is_file():raise SystemExit('Qualified update missing')
changes=[]
for c in ['brad','steve']:
 env=pathlib.Path('/etc/career-ops/'+c+'.env');unit=pathlib.Path('/etc/systemd/system/careerops-'+c+'.service')
 before=env.read_text();assert 'CAREER_OPS_ROOT=/var/lib/career-ops/'+c+'\n' in before
 after,count=re.subn(r'^CAREER_OPS_CODE_ROOT=.*$', 'CAREER_OPS_CODE_ROOT='+str(release),before,flags=re.M);assert count==1
 changes.append((env,before,after))
 before=unit.read_text();after,count=re.subn(r'^WorkingDirectory=.*$', 'WorkingDirectory='+str(release/'web'),before,flags=re.M);assert count==1
 changes.append((unit,before,after))
try:
 for file,before,after in changes:file.write_text(after)
 subprocess.run(['systemctl','daemon-reload'],check=True)
 subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'],check=True)
 for c,port in [('brad',3921),('steve',3922)]:
  subprocess.run(['systemctl','is-active','--quiet','careerops-'+c],check=True)
  for attempt in range(20):
   try:urllib.request.urlopen('http://127.0.0.1:'+str(port)+'/'+c+'/workspace/api/hosted',timeout=2)
   except urllib.error.HTTPError as error:
    if error.code==401:break
   except OSError:pass
   time.sleep(1)
  else:raise RuntimeError('Editor startup did not qualify')
except BaseException:
 for file,before,after in changes:file.write_text(before)
 subprocess.run(['systemctl','daemon-reload']);subprocess.run(['systemctl','restart','careerops-brad','careerops-steve'])
 raise
print('Direct edit-and-save update activated. Candidate data, history and shared login preserved.')
