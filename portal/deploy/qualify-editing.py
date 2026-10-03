#!/usr/bin/env python3
"""Qualify only fictional loopback workspaces. Never installs production services."""
import base64,pathlib,os,subprocess,tempfile,json,time,urllib.request,urllib.error,hashlib
base=pathlib.Path('/home/codex-deploy/apps/career-ops-editor');release=base/'releases/20261002-phase2a-01';processes=[];results={}
def request(port,candidate,path='',method='GET',body=None,token=True):
 headers={'X-Career-Gateway':'disposable-staging-only'} if token else {}
 if body is not None:headers['Content-Type']='application/json'
 req=urllib.request.Request(f'http://127.0.0.1:{port}/{candidate}/workspace'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
 try:
  with urllib.request.urlopen(req,timeout=10) as res:return res.status,res.read(),dict(res.headers)
 except urllib.error.HTTPError as error:return error.code,error.read(),dict(error.headers)
try:
 with tempfile.TemporaryDirectory(prefix='career-qualification-') as tmp:
  for candidate,port in [('brad',49321),('steve',49322)]:
   root=pathlib.Path(tmp)/candidate
   for d in ['config','modes','data']:(root/d).mkdir(parents=True,exist_ok=True)
   (root/'cv.md').write_text('# Fictional '+candidate+'\n')
   (root/'config/profile.yml').write_text('candidate:\n  full_name: Fictional '+candidate+'\ntarget_roles:\n  primary: [Engineer]\ncompensation:\n  minimum: $125K\n  target_range: $150K\n')
   (root/'modes/_profile.md').write_text('# Profile\n\n## Compensation\n\n$125K\n\n## Evidence\n\nFictional testing only.\n')
   (root/'data/applications.md').write_text('# Applications\n\n| # | Date | Company | Role | Score | Status | PDF | Report | Notes |\n|---|---|---|---|---|---|---|---|---|\n| 1 | 2026-10-02 | Fictional Co | Engineer | 4.0/5 | Evaluated | ❌ | — | baseline |\n')
   env={**os.environ,'NEXT_TELEMETRY_DISABLED':'1','CAREER_OPS_HOSTED':'1','NEXT_PUBLIC_HOSTED_MODE':'1','NEXT_PUBLIC_HOSTED_BASE':f'/{candidate}/workspace','BUILD_DIST':'.next-'+candidate,'CAREER_OPS_CANDIDATE':candidate,'CAREER_OPS_ROOT':str(root),'CAREER_OPS_CODE_ROOT':str(release),'CAREER_OPS_GATEWAY_TOKEN':'disposable-staging-only'}
   process=subprocess.Popen(['/usr/bin/node','node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port',str(port)],cwd=release/'web',env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);processes.append(process)
   for attempt in range(30):
    try:
     status,data,headers=request(port,candidate,'/api/hosted')
     if status==200:break
    except (OSError,urllib.error.URLError):pass
    time.sleep(1)
   else:raise RuntimeError('Staged server did not become healthy')
   state=json.loads(data);assert state['candidate']==candidate
   assert request(port,candidate,'/api/hosted',token=False)[0]==401
   assert request(port,candidate,'/api/hosted','POST',{'action':'cv'},token=False)[0]==401
   assert json.loads(request(port,candidate,'/api/hosted?candidate=other&root=/var/lib/career-ops/other')[1])['candidate']==candidate
   before=hashlib.sha256((root/'cv.md').read_bytes()).hexdigest()
   disabled=['/api/'+str(f.parent.relative_to(release/'web/src/app/api')) for f in (release/'web/src/app/api').rglob('route.ts') if f.parent.name!='hosted']
   for path in disabled+['/api/run','/api/assistant','/api/explore','/api/cv/ingest','/api/tracker/delete','/api/apply/fill','/_next/image','/config','/../steve/workspace/api/hosted']:
    for method in ['GET','POST']:assert request(port,candidate,path,method,{} if method=='POST' else None)[0] in (403,404)
   assert request(port,candidate,'/api/hosted','POST',{'action':'cv','revision':state['revision'],'content':'# Revised fictional '+candidate+'\n'})[0]==200
   assert request(port,candidate,'/api/hosted','POST',{'action':'cv','revision':state['revision'],'content':'stale'})[0]==409
   current=json.loads(request(port,candidate,'/api/hosted')[1]);assert candidate in current['contents']['cv.md']
   tracker_response=request(port,candidate,'/api/hosted','POST',{'action':'tracker','n':'1','status':'Applied','note':'fictional test','trackerRevision':current['trackerRevision']})
   if tracker_response[0]!=200:
    diagnostic=subprocess.run(['/usr/bin/node',str(release/'set-status.mjs'),'--row','1','Applied','--json'],env=env,capture_output=True,text=True);print(diagnostic.stdout,diagnostic.stderr);raise RuntimeError(str(tracker_response[:2]))
   assert '\tweb\t' in (root/'data/status-log.tsv').read_text()
   export=json.loads(request(port,candidate,'/api/hosted?export=1')[1]);assert all(not f['path'].startswith('.hosted') for f in export['files'])
   page=request(port,candidate);assert page[0]==200 and "'nonce-" in {k.lower():v for k,v in page[2].items()}['content-security-policy']
   subprocess.run(['/usr/bin/python3',str(release/'portal/deploy/candidate-backup.py'),str(root),str(root/'.hosted/backups'),'--drill'],check=True,stdout=subprocess.DEVNULL)
   rss=pathlib.Path(f'/proc/{process.pid}/status').read_text().split('VmRSS:')[1].splitlines()[0].strip()
   results[candidate]={'qualified':True,'pid_rss':rss,'base_path':f'/{candidate}/workspace','fictional_only':True}
  # Both processes remain alive concurrently and a restart preserves the scratch save.
  assert all(p.poll() is None for p in processes)
  for candidate in ['brad','steve']:assert candidate in (pathlib.Path(tmp)/candidate/'cv.md').read_text()
  # Exercise shared authentication and exact routing with this VPS's Caddy.
  croot=pathlib.Path(tmp)/'gateway';croot.mkdir()
  hashed=subprocess.check_output(['caddy','hash-password','--plaintext','disposable-caddy-test'],text=True).strip()
  (croot/'auth').write_text('basicauth {\n careerops '+hashed+'\n}\n')
  config=(release/'portal/deploy/install-editing.sh').read_text().split('cat > "$site" <<EOF\n')[1].split('\nEOF')[0]
  config=config.replace('careerops.steveleclair.info {','http://127.0.0.1:49320 {').replace('/etc/caddy/private/careerops-auth.caddy',str(croot/'auth'))
  for candidate,port in [('brad',49321),('steve',49322)]:
   (croot/candidate).write_text('reverse_proxy 127.0.0.1:'+str(port)+' {\n header_up X-Career-Gateway disposable-staging-only\n}\n')
   config=config.replace('/etc/caddy/private/careerops-'+candidate+'-gateway.caddy',str(croot/candidate)).replace('handle @'+candidate+' { import '+str(croot/candidate)+' }','handle @'+candidate+' {\n import '+str(croot/candidate)+'\n }')
  (croot/'Caddyfile').write_text('{\n admin off\n auto_https off\n}\n'+config)
  gateway=subprocess.Popen(['caddy','run','--config',str(croot/'Caddyfile'),'--adapter','caddyfile'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);processes.append(gateway)
  time.sleep(2)
  authorization='Basic '+base64.b64encode(b'careerops:disposable-caddy-test').decode()
  for candidate in ['brad','steve']:
   url='http://127.0.0.1:49320/'+candidate+'/workspace/api/hosted'
   try:urllib.request.urlopen(url);raise AssertionError('Unauthenticated API exposed')
   except urllib.error.HTTPError as error:assert error.code==401
   with urllib.request.urlopen(urllib.request.Request(url,headers={'Authorization':authorization})) as response:assert json.loads(response.read())['candidate']==candidate
   req=urllib.request.Request(url.replace('/api/hosted','/api/run'),data=b'{}',headers={'Authorization':authorization,'Content-Type':'application/json'})
   try:urllib.request.urlopen(req);raise AssertionError('Worker exposed')
   except urllib.error.HTTPError as error:assert error.code==403
  processes[1].terminate();processes[1].wait(timeout=10)
  restarted=subprocess.Popen(['/usr/bin/node','node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port','49322'],cwd=release/'web',env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);processes[1]=restarted
  time.sleep(2)
  assert 'Revised fictional steve' in json.loads(request(49322,'steve','/api/hosted')[1])['contents']['cv.md']
  results['steve']['restart_preserved_save']=True
  results['gateway']={'shared_auth':'verified with disposable login','caddy_routing':'passed'}
  (base/'qualification.json').write_text(json.dumps(results,indent=2))
  print(json.dumps(results))
finally:
 for process in processes:
  process.terminate()
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
