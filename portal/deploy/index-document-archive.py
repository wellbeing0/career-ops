#!/usr/bin/env python3
"""Owner-run index of the currently published historical snapshot; no candidate document copies."""
import hashlib,json,os,pathlib,pwd,urllib.parse,uuid,time,datetime
if os.geteuid()!=0:raise SystemExit('Run with sudo')
base=pathlib.Path('/home/codex-deploy/apps/career-ops-portal/current').resolve()
if not base.is_relative_to(pathlib.Path('/home/codex-deploy/apps/career-ops-portal/releases')):raise SystemExit('Unexpected archive source')
manifest=json.loads((base/'manifest.json').read_text())
for c in ['brad','steve']:
 documents=[]
 for f in manifest['files']:
  prefix='site/'+c+'/files/'
  if not f['path'].startswith(prefix):continue
  p=base/f['path'];rel=f['path'][len(prefix):]
  if p.is_symlink() or not p.resolve().is_relative_to(base):raise SystemExit('Unsafe archive source')
  data=p.read_bytes()
  if hashlib.sha256(data).hexdigest()!=f['sha256']:raise SystemExit('Archive checksum mismatch')
  stat=p.stat();documents.append({'path':rel,'href':'/'+c+'/files/'+urllib.parse.quote(rel,safe="/~!*'()"),'modifiedAt':__import__('datetime').datetime.fromtimestamp(stat.st_mtime,__import__('datetime').timezone.utc).isoformat(),'size':stat.st_size,'extension':p.suffix[1:].lower()})
 root=pathlib.Path('/var/lib/career-ops/'+c);target=root/'.hosted/document-archive-index.json';owner=pwd.getpwnam('careerops-'+c);payload=json.dumps({'candidate':c,'snapshotAt':manifest['snapshot_at'],'archiveRelease':base.name,'documents':documents})
 lockfile=root/'.hosted/edit.lock';fd=None
 for attempt in range(50):
  try:fd=os.open(lockfile,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);break
  except FileExistsError:time.sleep(.1)
 if fd is None:raise SystemExit('Workspace busy; retry activation to complete archive indexing')
 try:
  os.write(fd,json.dumps({'pid':os.getpid(),'at':datetime.datetime.now(datetime.timezone.utc).isoformat()}).encode());os.fchown(fd,owner.pw_uid,owner.pw_gid)
  if target.exists() and target.read_text()==payload:print(json.dumps({'candidate':c,'archivedDocuments':len(documents),'changed':False}));continue
  if target.exists():
   old=root/'.hosted'/('document-archive-index-'+uuid.uuid4().hex+'.previous.json');old.write_text(target.read_text());old.chmod(0o600);os.chown(old,owner.pw_uid,owner.pw_gid)
  temp=target.with_name(target.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_text(payload);temp.chmod(0o600);os.chown(temp,owner.pw_uid,owner.pw_gid);os.replace(temp,target)
  print(json.dumps({'candidate':c,'archivedDocuments':len(documents),'changed':True}))
 finally:os.close(fd);lockfile.unlink()
