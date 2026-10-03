"""Credential-reference regression uses fictional values and never opens a store."""
import pathlib,subprocess,unittest
class GatewayTokenTests(unittest.TestCase):
 def test_native_reference_boundary(self):
  uri=(pathlib.Path(__file__).resolve().parents[1]/'deploy/resolve-gateway-token.mjs').as_uri()
  script="""import assert from 'node:assert/strict';
import {gatewayToken} from '%s';
const c={gateway:{auth:{mode:'token',token:{source:'store',provider:'default',id:'FICTIONAL_TOKEN'}}}};
assert.equal(await gatewayToken(c,async(ref,options)=>{assert.equal(ref.id,'FICTIONAL_TOKEN');assert.equal(options.config,c);return 'fictional-token-long-enough';}),'fictional-token-long-enough');
await assert.rejects(gatewayToken({gateway:{auth:{mode:'token',token:{source:'exec',provider:'default',id:'UNTRUSTED'}}}},()=>{throw Error('must not invoke');}));
await assert.rejects(gatewayToken(c,async()=> 'bad\\nvalue'));
"""%uri
  subprocess.run(['node','--input-type=module','-'],input=script,text=True,check=True,capture_output=True)
