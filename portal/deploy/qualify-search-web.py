#!/usr/bin/env python3
"""Staged HTTP/mobile checks with fictional roots, disposable auth and mocked public boards."""
import argparse,json,os,pathlib,shutil,socket,subprocess,time,urllib.request,urllib.error
p=argparse.ArgumentParser();p.add_argument('release',type=pathlib.Path);p.add_argument('--dist-prefix',default='.next');a=p.parse_args();a.release=a.release.resolve();processes=[];ports={};results={}
fixture=json.loads(subprocess.check_output(['node',str(a.release/'portal/deploy/qualify-search.mjs'),str(a.release),'--keep'],text=True))['fixture'];scratch=pathlib.Path(fixture['temporaryRoot'])
def request(c,path,method='GET',body=None,token=True,origin=None):
 headers={'X-Career-Gateway':'fictional-search-gateway'} if token else {}
 if origin:headers['Origin']=origin
 if body is not None:headers['Content-Type']='application/json'
 req=urllib.request.Request(f'http://127.0.0.1:{ports[c]}/{c}/workspace'+path,data=json.dumps(body).encode() if body is not None else None,headers=headers,method=method)
 try:
  with urllib.request.urlopen(req,timeout=25) as response:return response.status,json.loads(response.read()) if 'application/json' in response.headers.get('Content-Type','') else response.read().decode()
 except urllib.error.HTTPError as error:return error.code,error.read().decode()
try:
 for c in ['brad','steve']:
  with socket.socket() as sock:sock.bind(('127.0.0.1',0));ports[c]=sock.getsockname()[1]
  env={**os.environ,'CAREER_OPS_HOSTED':'1','NEXT_PUBLIC_HOSTED_MODE':'1','NEXT_PUBLIC_HOSTED_BASE':f'/{c}/workspace','CAREER_OPS_CANDIDATE':c,'CAREER_OPS_ROOT':fixture[c+'Root'],'CAREER_OPS_CODE_ROOT':fixture['code'],'CAREER_OPS_GATEWAY_TOKEN':'fictional-search-gateway','BUILD_DIST':a.dist_prefix+'-'+c,'NEXT_TELEMETRY_DISABLED':'1'}
  log=(scratch/(c+'-web.log')).open('w');process=subprocess.Popen(['node','node_modules/next/dist/bin/next','start','--hostname','127.0.0.1','--port',str(ports[c])],cwd=a.release/'web',env=env,stdout=log,stderr=log);processes.append(process)
  for attempt in range(40):
   try:
    if request(c,'/api/hosted/search')[0]==200:break
   except OSError:pass
   time.sleep(.25)
  else:raise RuntimeError(c+' server failed: '+(scratch/(c+'-web.log')).read_text()[-1500:])
  assert request(c,'/api/hosted/search',token=False)[0]==401
  for route in ['/api/run','/api/explore','/api/apply/fill','/api/tracker/delete']:
   assert request(c,route,'POST',{})[0]==403
  assert request(c,'/api/hosted/search','POST',{'action':'start','key':'bad'},origin='https://untrusted.example')[0]==403
  root=pathlib.Path(fixture[c+'Root']);(root/'.hosted/document-archive-index.json').write_text(json.dumps({'candidate':c,'snapshotAt':'Oct 02, 2026','documents':[{'path':'cv.md','href':'/'+c+'/files/cv.md','modifiedAt':'2026-10-02T12:00:00Z','size':15,'extension':'md'}]}))
  catalog=request(c,'/api/hosted/documents')[1];assert catalog['candidate']==c and catalog['archiveAvailable']
  current=next(d for d in catalog['documents'] if d['source']=='current' and d['path']=='cv.md')
  assert request(c,'/api/hosted/documents?id='+current['id'])[0]==200
  assert request(c,'/api/hosted/documents?id=../cv.md')[0]==409
  assert request(c,'/api/hosted/documents','POST',{})[0]==403
  assert request(c,'/api/hosted/documents',origin='https://untrusted.example')[0]==403
  state=request(c,'/api/hosted/search')[1];assert state['candidate']==c
  assert request(c,'/api/hosted/search?id='+state['run']['id']+'&report=1')[0]==200
  results[c]={'loopbackPort':ports[c],'auth':'passed','blockedWorkers':'passed','savedResults':'passed','reportDownload':'passed'}
 browser_script=scratch/'mobile.mjs'
 browser_script.write_text("""
import {createRequire} from 'node:module';import assert from 'node:assert/strict';
const require=createRequire(process.argv[2]+'/web/package.json');const {chromium}=require('playwright-core');const ports=JSON.parse(process.argv[3]);
const browser=await chromium.launch({executablePath:process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':'/usr/bin/google-chrome',headless:true,args:['--no-sandbox']});
try{const context=await browser.newContext({viewport:{width:390,height:844},extraHTTPHeaders:{'X-Career-Gateway':'fictional-search-gateway'}});const errors=[];context.on('page',p=>p.on('pageerror',e=>errors.push(e.message)));let page=await context.newPage();let dialogs=0;page.on('dialog',async d=>{dialogs++;await d.dismiss();});
await page.goto('http://127.0.0.1:'+ports.brad+'/brad/workspace');await page.getByRole('button',{name:'Search',exact:true}).click();await page.getByText('Search opportunities',{exact:true}).waitFor();await page.getByText('Senior Frontend Engineer 3',{exact:false}).waitFor();const checkbox=page.getByRole('checkbox').filter({visible:true});const available=page.locator('article input[type=checkbox]:not([disabled])');await available.first().check();await page.getByRole('button',{name:/Add selected jobs to pipeline/}).click();await page.getByText('1 new job(s) added to your pipeline. No application was sent.',{exact:true}).waitFor();assert.equal(dialogs,0);assert.ok(await page.getByRole('link',{name:'Download search report'}).isVisible());assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
await page.getByRole('button',{name:/Existing opportunities/}).click();await page.getByRole('heading',{name:'Existing opportunities',exact:true}).waitFor();assert.ok(await page.getByText('Availability unverified',{exact:false}).count()>0);await page.getByRole('button',{name:/Existing opportunities/}).click();
await page.getByRole('button',{name:'View / edit job filters',exact:true}).click();const include=page.getByRole('textbox',{name:'Include title keywords',exact:true});await include.waitFor();const original=await include.inputValue();await include.fill(original+'\\nAI Architect');await page.getByRole('button',{name:'Save filters',exact:true}).click();await page.getByText('Filters saved. The previous version is backed up. Start another search to use these rules.',{exact:true}).waitFor();await page.getByText('Previous filter versions (1)',{exact:true}).click();await page.getByRole('button',{name:/Restore filters from/}).click();await page.getByText('Filters restored. The previous version is backed up.',{exact:true}).waitFor();assert.equal(await include.inputValue(),original);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));await page.getByRole('button',{name:'View / edit job filters',exact:true}).click();
await page.getByRole('button',{name:'Documents',exact:true}).click();await page.getByRole('heading',{name:'Documents',exact:true}).waitFor();await page.getByRole('combobox',{name:'Document source',exact:true}).selectOption('archive');await page.getByRole('link',{name:'View archived document',exact:true}).first().waitFor();await page.getByRole('combobox',{name:'Document source',exact:true}).selectOption('current');await page.getByRole('textbox',{name:'Find documents',exact:true}).fill('search-reports');await page.getByRole('button',{name:'View document',exact:true}).first().click();await page.getByRole('button',{name:'Close document preview',exact:true}).waitFor();await page.getByRole('button',{name:'Close document preview',exact:true}).click();await page.getByRole('button',{name:'Show all documents',exact:true}).click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));
await page.getByRole('button',{name:'Pipeline',exact:true}).click();await page.getByRole('heading',{name:'Pipeline',exact:true}).waitFor();await page.getByRole('textbox',{name:'Find saved opportunities',exact:true}).fill('good');await page.getByText('Senior Frontend Engineer',{exact:false}).first().waitFor();await page.getByRole('button',{name:'Refresh pipeline',exact:true}).click();assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth));await page.getByRole('button',{name:'Profile/CV recovery',exact:true}).click();await page.getByRole('heading',{name:'Profile/CV recovery',exact:true}).waitFor();
await page.reload();await page.getByRole('button',{name:'Search',exact:true}).click();await page.getByText('Search opportunities',{exact:true}).waitFor();assert.ok(await page.locator('article input[type=checkbox][disabled]:checked').count()>=2);
await page.goto('http://127.0.0.1:'+ports.steve+'/steve/workspace?view=documents');await page.getByRole('heading',{name:'Documents',exact:true}).waitFor();await page.getByRole('button',{name:'Pipeline',exact:true}).click();await page.getByRole('heading',{name:'Pipeline',exact:true}).waitFor();await page.getByRole('button',{name:'Search',exact:true}).click();await page.getByRole('button',{name:'Start free search'}).click();await page.getByRole('button',{name:'Cancel search'}).waitFor();await page.close();await new Promise(r=>setTimeout(r,4500));page=await context.newPage();await page.goto('http://127.0.0.1:'+ports.steve+'/steve/workspace');await page.getByRole('button',{name:'Pipeline',exact:true}).click();await page.getByRole('heading',{name:'Pipeline',exact:true}).waitFor();await page.getByRole('button',{name:'Search',exact:true}).click();await page.getByRole('button',{name:'Start free search'}).waitFor();await page.waitForFunction(()=>!document.querySelector('button')?.disabled);await page.getByRole('button',{name:'Start free search'}).click();await page.getByRole('button',{name:'Cancel search'}).click();await page.getByText('Cancellation requested. Saved results will remain available.',{exact:true}).waitFor();assert.equal(errors.length,0);console.log(JSON.stringify({mobileViewport:'390x844',documentLibrary:'passed',archiveFilter:'passed',liveReportPreview:'passed',pipelineNavigation:'passed',recoveryLabel:'passed',existingOpportunities:'passed',filterSaveRestore:'passed',selection:'passed',reload:'passed',disconnect:'passed',cancel:'passed',pageErrors:errors.length,saveDialogs:dialogs}));
}finally{await browser.close();}
""")
 mobile=json.loads(subprocess.check_output(['node',str(browser_script),str(a.release),json.dumps(ports)],text=True));results['mobile']=mobile
 for c,process in zip(['brad','steve'],processes):
  status=pathlib.Path(f'/proc/{process.pid}/status')
  if status.exists():results[c]['webRss']=status.read_text().split('VmRSS:')[1].splitlines()[0].strip()
 print(json.dumps(results))
finally:
 for process in processes:
  process.terminate()
  try:process.wait(timeout=10)
  except subprocess.TimeoutExpired:process.kill();process.wait()
 shutil.rmtree(scratch,ignore_errors=True)
