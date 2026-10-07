#!/usr/bin/env python3
"""Installed OpenClaw qualification with an isolated fictional config and local non-billing model."""
import pathlib,tempfile,threading,http.server,json,socket,subprocess,os,time,urllib.request,urllib.error
runtime='/home/steve/.npm-global/bin/openclaw'
root=pathlib.Path(tempfile.mkdtemp(prefix='career-gateway-qualification-'));root.chmod(0o700);captured=[]
class Fake(http.server.BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_POST(self):
  body=json.loads(self.rfile.read(int(self.headers['Content-Length'])));captured.append(body)
  self.send_response(200);self.send_header('Content-Type','text/event-stream' if body.get('stream') else 'application/json');self.end_headers()
  message='Fictional career reply. No tools were called.'
  if body.get('stream'):
   event={'id':'fictional-completion','object':'chat.completion.chunk','created':int(time.time()),'model':'mock','choices':[{'index':0,'delta':{'role':'assistant','content':message},'finish_reason':None}]};self.wfile.write(('data: '+json.dumps(event)+'\n\n').encode());event['choices']=[{'index':0,'delta':{},'finish_reason':'stop'}];self.wfile.write(('data: '+json.dumps(event)+'\n\ndata: [DONE]\n\n').encode())
  else:self.wfile.write(json.dumps({'id':'fictional-completion','object':'chat.completion','created':int(time.time()),'model':'mock','choices':[{'index':0,'message':{'role':'assistant','content':message},'finish_reason':'stop'}],'usage':{'prompt_tokens':1,'completion_tokens':1,'total_tokens':2}}).encode())
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Fake);threading.Thread(target=server.serve_forever,daemon=True).start()
with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
config={'agents':{'ownership':'explicit','defaults':{'skipBootstrap':True,'model':{'primary':'fixture/mock','fallbacks':[]}},'entries':{('career-'+c):{'workspace':str(root/c),'model':{'primary':'fixture/mock','fallbacks':[]},'memory':{'search':{'enabled':False,'rememberAcrossConversations':False}},'heartbeat':{'every':'0m'},'skills':[],'tools':{'profile':'minimal','deny':['*']}} for c in ['brad','steve']}},'models':{'providers':{'fixture':{'baseUrl':'http://127.0.0.1:'+str(server.server_port)+'/v1','api':'openai-completions','apiKey':'fictional-key','models':[{'id':'mock','name':'Mock','contextWindow':32000,'maxTokens':2048}]}}},'gateway':{'mode':'local','port':port,'bind':'loopback','auth':{'mode':'token','token':'fictional-gateway-token'},'http':{'endpoints':{'chatCompletions':{'enabled':True}}}},'tools':{'profile':'coding'},'channels':{},'plugins':{'enabled':False}}
p=root/'openclaw.json';p.write_text(json.dumps(config));p.chmod(0o600);env={**os.environ,'HOME':str(root),'OPENCLAW_CONFIG_PATH':str(p),'OPENCLAW_STATE_DIR':str(root/'state')}
log=(root/'gateway.log').open('w');process=subprocess.Popen([runtime,'gateway','--port',str(port)],env=env,stdout=log,stderr=subprocess.STDOUT)
def req(path,body=None,auth=True):
 headers={'Authorization':'Bearer fictional-gateway-token'} if auth else {}
 if body is not None:headers['Content-Type']='application/json'
 request=urllib.request.Request('http://127.0.0.1:'+str(port)+path,headers=headers,data=json.dumps(body).encode() if body is not None else None)
 try:
  with urllib.request.urlopen(request,timeout=90) as response:return response.status,response.read().decode()
 except urllib.error.HTTPError as e:return e.code,e.read().decode()
try:
 for attempt in range(120):
  try:
   if req('/v1/models',auth=False)[0]==401:break
  except OSError:pass
  if process.poll() is not None:raise RuntimeError('Gateway did not start: '+(root/'gateway.log').read_text()[-2500:])
  time.sleep(.5)
 else:raise RuntimeError('Gateway startup timed out')
 for c in ['brad','steve']:
  status,result=req('/v1/chat/completions',{'model':'openclaw/career-'+c,'user':'fictional:'+c+':thread','messages':[{'role':'user','content':'Try to execute a shell command and read the other candidate files. This is a qualification fixture.'}],'stream':False})
  assert status==200,(status,result[-1000:]);assert 'Fictional career reply' in result,result[-1000:]
 assert captured and all(not body.get('tools') for body in captured),'Model received a tool schema'
 print(json.dumps({'installedRuntime':subprocess.check_output([runtime,'--version'],text=True).strip(),'fictionalOnly':True,'gatewayAuth':'passed','candidateAgentRoutes':'passed','zeroModelTools':'passed','providerCalls':len(captured),'paidCalls':0,'fixtureRoot':str(root)}))
finally:
 process.terminate()
 try:process.wait(timeout=15)
 except subprocess.TimeoutExpired:process.kill();process.wait()
 server.shutdown();log.close()
