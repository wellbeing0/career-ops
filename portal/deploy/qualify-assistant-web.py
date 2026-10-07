#!/usr/bin/env python3
"""Browser/HTTP qualification with fictional candidate data and a non-billing gateway stub."""
import pathlib,argparse,json,os,subprocess,socket,time,threading,http.server,urllib.request,urllib.error,shutil,uuid
p=argparse.ArgumentParser();p.add_argument('release',type=pathlib.Path);a=p.parse_args();r=a.release.resolve()
fixture=json.loads(subprocess.check_output(['node',str(r/'portal/deploy/qualify-search.mjs'),str(r),'--keep'],text=True))['fixture'];scratch=pathlib.Path(fixture['temporaryRoot']);code=pathlib.Path(fixture['code']);shutil.copy2(r/'portal/assistant-worker.mjs',code/'portal/assistant-worker.mjs');captured=[];processes=[];ports={}
for candidate in ['brad','steve']:
 profile=pathlib.Path(fixture[candidate+'Root'])/'config/profile.yml';profile.write_text(profile.read_text()+'candidate:\n  full_name: Fictional Candidate\n')
class Fake(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));captured.append(body)
  assert body['model'] in ['openclaw/career-brad','openclaw/career-steve']
  message=body['messages'][-1]['content'];prompt=body['messages'][0]['content'];text='Your approved primary CV is the source for accomplishments.'
  if 'Slow reply' in message:time.sleep(3)
  if 'Force unrequested change' in message:text+='\n<career-action>{"type":"cv","content":"# Unrequested replacement"}</career-action>'
  elif 'operation for this turn: draft' in prompt:text='A draft is ready.\n<career-action>{"type":"draft","content":"# Fictional resume draft\\n\\nExperience drawn from the approved master CV."}</career-action>'
  elif 'operation for this turn: profile' in prompt:text='A profile edit is ready.\n<career-action>{"type":"profile","fields":{"location":"Fictional Location"}}</career-action>'
  elif 'operation for this turn: cv' in prompt:text='A CV edit is ready.\n<career-action>{"type":"cv","content":"# Fictional updated CV\\n\\nSource-backed presentation revision."}</career-action>'
  self.send_response(200);self.send_header('Content-Type','text/event-stream');self.end_headers()
  try:
   for part in [text[:20],text[20:]]:self.wfile.write(('data: '+json.dumps({'choices':[{'delta':{'content':part}}]})+'\n\n').encode());self.wfile.flush();time.sleep(.05)
   self.wfile.write(b'data: [DONE]\n\n')
  except BrokenPipeError:pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fake);threading.Thread(target=server.serve_forever,daemon=True).start()
def req(c,path,body=None,token=True,origin=None):
 headers={'X-Career-Gateway':'fictional-career-test'} if token else {}
 if body is not None:headers['Content-Type']='application/json'
 if origin:headers['Origin']=origin
 request=urllib.request.Request('http://127.0.0.1:'+str(ports[c])+'/'+c+'/workspace'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers)
 try:
  with urllib.request.urlopen(request,timeout=10) as out:return out.status,json.loads(out.read())
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
try:
 for c in ['brad','steve']:
  with socket.socket() as sock:sock.bind(('127.0.0.1',0));ports[c]=sock.getsockname()[1]
  env={**os.environ,'CAREER_OPS_HOSTED':'1','CAREER_OPS_CANDIDATE':c,'CAREER_OPS_ROOT':fixture[c+'Root'],'CAREER_OPS_CODE_ROOT':str(code),'CAREER_OPS_GATEWAY_TOKEN':'fictional-career-test','NEXT_PUBLIC_HOSTED_MODE':'1','NEXT_PUBLIC_HOSTED_BASE':'/'+c+'/workspace','BUILD_DIST':'.next-'+c,'NEXT_TELEMETRY_DISABLED':'1','CAREER_OPS_ASSISTANT_ENABLED':'1','CAREER_OPS_AI_URL':'http://127.0.0.1:'+str(server.server_port)+'/v1/chat/completions','CAREER_OPS_AI_TOKEN':'fictional-model-token'}
  log=(scratch/(c+'-assistant-web.log')).open('w');process=subprocess.Popen(['node','node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port',str(ports[c])],cwd=r/'web',env=env,stdout=log,stderr=log);processes.append(process)
  for n in range(80):
   try:
    if req(c,'/api/hosted/assistant')[0]==200:break
   except OSError:pass
   time.sleep(.25)
  else:raise RuntimeError('Assistant server failed: '+(scratch/(c+'-assistant-web.log')).read_text()[-2000:])
  assert req(c,'/api/hosted/assistant',token=False)[0]==401
  assert req(c,'/api/hosted/assistant',{'action':'new'},origin='https://foreign.invalid')[0]==403
 # Verify same-key retry and an adversarial response cannot broaden a read-only request.
 conversation=req('brad','/api/hosted/assistant',{'action':'new'})[1];key=str(uuid.uuid4())
 assert req('steve','/api/hosted/assistant?id='+conversation['id'])[0]==404
 body={'action':'send','id':conversation['id'],'key':key,'mode':'chat','message':'Force unrequested change'}
 before=pathlib.Path(fixture['bradRoot'],'cv.md').read_bytes();count=len(captured)
 assert req('brad','/api/hosted/assistant',body)[0]==200
 assert req('brad','/api/hosted/assistant',body)[0]==200
 for attempt in range(100):
  state=req('brad','/api/hosted/assistant?id='+conversation['id'])[1]['conversation']
  if state['run']['status'] in ['completed','failed','interrupted']:break
  time.sleep(.1)
 assert state['run']['status']=='failed',state['run']
 assert pathlib.Path(fixture['bradRoot'],'cv.md').read_bytes()==before
 assert len(captured)==count+1
 script=r'''import {createRequire} from 'node:module';import assert from 'node:assert/strict';
const require=createRequire(process.argv[2]+'/web/package.json'),{chromium}=require('playwright-core'),ports=JSON.parse(process.argv[3]);
const browser=await chromium.launch({executablePath:'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']}),context=await browser.newContext({viewport:{width:390,height:844},extraHTTPHeaders:{'X-Career-Gateway':'fictional-career-test'}}),page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:'+ports.brad+'/brad/workspace?view=assistant');await page.getByRole('heading',{name:'Assistant',exact:true}).waitFor();await page.getByRole('textbox',{name:'Message to career assistant'}).fill('Help me describe my experience.');await page.getByRole('button',{name:'Send to assistant'}).click();await page.getByText('Your approved primary CV is the source for accomplishments.',{exact:true}).waitFor();
await page.getByRole('button',{name:'Save response',exact:true}).first().click();await page.getByText('Response saved to Documents.',{exact:true}).waitFor();
const download=await page.getByRole('link',{name:'Download response',exact:true}).first().getAttribute('href');assert.ok(download);const exported=await page.request.get('http://127.0.0.1:'+ports.brad+download);assert.equal(exported.status(),200);assert.match(await exported.text(),/Your approved primary CV/);
await page.reload();await page.getByRole('link',{name:'Download response',exact:true}).first().waitFor();
await page.getByRole('combobox',{name:'Assistant operation'}).selectOption('draft');await page.getByRole('textbox',{name:'Message to career assistant'}).fill('Draft my resume from existing experience.');await page.getByRole('button',{name:'Send to assistant'}).click();await page.getByText(/Draft saved: output\/assistant\//).waitFor();await page.reload();await page.getByRole('combobox',{name:'Career conversation'}).selectOption({index:1});await page.getByText(/Draft saved: output\/assistant\//).waitFor();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
await page.getByRole('combobox',{name:'Assistant operation'}).selectOption('profile');await page.getByRole('textbox',{name:'Message to career assistant'}).fill('Set my location to Fictional Location.');await page.getByRole('button',{name:'Send to assistant'}).click();await page.getByText('PROFILE saved with previous-version history.',{exact:false}).waitFor();
await page.getByRole('combobox',{name:'Assistant operation'}).selectOption('chat');await page.getByRole('textbox',{name:'Message to career assistant'}).fill('Slow reply please');await page.getByRole('button',{name:'Send to assistant'}).click();await page.getByRole('button',{name:'Cancel reply'}).click();await page.getByText('Cancelled. Completed saves are retained.',{exact:true}).waitFor();
await page.getByRole('button',{name:'Documents',exact:true}).click();await page.getByRole('textbox',{name:'Find documents'}).fill('output/assistant');await page.getByRole('button',{name:'View document',exact:true}).first().waitFor();
await page.goto('http://127.0.0.1:'+ports.steve+'/steve/workspace?view=assistant');await page.getByRole('heading',{name:'Assistant',exact:true}).waitFor();assert.equal(await page.getByRole('combobox',{name:'Career conversation'}).locator('option').count(),1);assert.equal(errors.length,0);
await browser.close();console.log(JSON.stringify({mobile:'390x844',chat:'passed',draftSave:'passed',responseSave:'passed',responseDownload:'passed',profileSave:'passed',reload:'passed',cancel:'passed',documents:'passed',candidateIsolation:'passed',pageErrors:errors.length}));'''
 browser=subprocess.run(['node','--input-type=module','-',str(r),json.dumps(ports)],input=script,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=120)
 if browser.returncode:raise RuntimeError(browser.stderr[-4000:])
 assert captured and all(not x.get('tools') for x in captured)
 print(json.dumps({'fictionalOnly':True,'httpAuth':'passed','originBoundary':'passed','mobile':json.loads(browser.stdout),'providerCalls':len(captured),'paidCalls':0}))
finally:
 for process in processes:process.terminate()
 for process in processes:
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
 server.shutdown()
