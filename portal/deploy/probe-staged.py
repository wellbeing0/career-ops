import base64,json,pathlib,subprocess,tempfile,time,urllib.request,urllib.error
base=pathlib.Path('/home/codex-deploy/apps/career-ops-portal');user='local-test';password='temporary-local-test-password-not-live'
hashvalue=subprocess.check_output(['caddy','hash-password'],input=password+'\n',text=True).strip()
installer=(base/'deploy/install-caddy.sh').read_text();config=installer.split('cat > "$staged" <<EOF\n',1)[1].split('\nEOF',1)[0]
with tempfile.TemporaryDirectory(prefix='career-portal-probe-') as tmp:
 temp=pathlib.Path(tmp);auth=temp/'auth.caddy';auth.write_text('basicauth {\n '+user+' '+hashvalue+'\n}\n')
 config=config.replace('$domain','http://127.0.0.1:8779').replace('$auth',str(auth)).replace('$base',str(base))
 p=temp/'Caddyfile';p.write_text('{\n admin off\n auto_https off\n}\n'+config)
 v=subprocess.run(['caddy','validate','--config',str(p),'--adapter','caddyfile'],capture_output=True,text=True)
 if v.returncode:raise RuntimeError(v.stderr)
 log=(temp/'log').open('w');proc=subprocess.Popen(['caddy','run','--config',str(p),'--adapter','caddyfile'],stdout=log,stderr=log)
 try:
  def request(path,method='GET',authenticated=False):
   headers={}
   if authenticated:headers['Authorization']='Basic '+base64.b64encode((user+':'+password).encode()).decode()
   req=urllib.request.Request('http://127.0.0.1:8779'+path,headers=headers,method=method)
   try:
    with urllib.request.urlopen(req,timeout=5) as res:return res.status,dict(res.headers),res.read() if method=='GET' else b''
   except urllib.error.HTTPError as e:return e.code,dict(e.headers),e.read()
  for i in range(40):
   try:request('/');break
   except urllib.error.URLError:time.sleep(.1)
  manifest=json.loads((base/'current/manifest.json').read_text());count=0
  from urllib.parse import quote
  for item in manifest['files']:
   route='/'+quote(item['path'][5:],safe='/')
   status,headers,body=request(route)
   if status!=401 or b'Brad Efting' in body:raise AssertionError((route,status))
   count+=1
  for route in ['/','/brad/','/steve/','/brad/view/cv.md.html','/steve/view/cv.md.html']:
   status,headers,body=request(route,authenticated=True)
   if status!=200:raise AssertionError((route,status))
   if "script-src 'none'" not in headers.get('Content-Security-Policy',''):raise AssertionError('CSP absent')
  for route in ['/manifest.json','/etc/caddy/private/careerops-auth.caddy','/brad/files/.env','/steve/files/output/migration-backup/old.md']:
   if request(route,authenticated=True)[0]!=404:raise AssertionError(route)
  if request('/brad/view/cv.md.html','POST',True)[0]!=405:raise AssertionError('Write not denied')
  for route in ['/brad/files/documents/cv/BradEfting_resume.pdf','/steve/files/cv.md']:
   if request(route,'HEAD',True)[0]!=200:raise AssertionError('Download unavailable '+route)
  print(json.dumps({'caddy_version':'2.6.2','config_validation':'passed','unauthenticated_files_challenged':count,'authenticated_candidate_navigation':'passed','authenticated_downloads':'passed','mutation_denial':'405','excluded_paths':'404','scope':'Temporary loopback-only test; production Caddy unchanged.'}))
 finally:
  proc.terminate();proc.wait(timeout=5);log.close()
