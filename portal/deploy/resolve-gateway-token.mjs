/** Private activation pipe only. Never invoke for diagnostics or display its output. */
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
const RESOLVERS=Object.freeze({'OpenClaw 2026.9.3 (1391f7c)':'resolve-C12j3-_H.mjs','OpenClaw 2026.9.8 (fc23bc8)':'resolve-ClJDvNkN.mjs'});
export function resolverForVersion(version){if(!Object.hasOwn(RESOLVERS,version))throw new Error('Unqualified OpenClaw version');return RESOLVERS[version];}
export async function gatewayToken(config,resolve){
 if(config.gateway?.auth?.mode!=='token')throw new Error('Unsupported authentication');
 const ref=config.gateway.auth.token;
 let token;
 if(typeof ref==='string')token=ref;
 else {
  if(!ref||ref.source!=='store'||ref.provider!==(config.secrets?.defaults?.store||'default')||! /^[A-Z][A-Z0-9_]{0,127}$/.test(ref.id||''))throw new Error('Unsupported credential reference');
  const explicit=config.secrets?.providers?.[ref.provider];
  if(explicit&&explicit.source!=='store')throw new Error('Unsupported credential provider');
  token=await resolve(ref,{config,env:process.env});
 }
 if(typeof token!=='string'||! /^[A-Za-z0-9_.:-]{20,512}$/.test(token))throw new Error('Invalid gateway token');
 return token;
}
if(process.argv[1]&&import.meta.url===pathToFileURL(process.argv[1]).href){
 try {
  const config=JSON.parse(fs.readFileSync('/home/steve/.openclaw/openclaw.json','utf8'));
  const version=execFileSync('/home/steve/.npm-global/bin/openclaw',['--version'],{encoding:'utf8',stdio:['ignore','pipe','pipe']}).trim();
  const {t:resolve}=await import('/home/steve/.npm-global/lib/node_modules/openclaw/dist/'+resolverForVersion(version));
  process.stdout.write(await gatewayToken(config,resolve));
 }catch{process.stderr.write('Existing gateway credential could not be resolved securely.\n');process.exitCode=1;}
}
