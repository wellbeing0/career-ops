#!/usr/bin/env python3
"""Approved Steve-only model alignment; validates natively and retains private rollback."""
import copy, datetime, json, os, pathlib, subprocess, time, urllib.request, urllib.error
RUNTIME='/home/steve/.npm-global/bin/openclaw'
VERSION='OpenClaw 2026.9.8 (fc23bc8)'

def aligned_config(original):
    result=copy.deepcopy(original)
    entries=result.get('agents',{}).get('entries',{})
    if set(entries)!={'main','career-brad','career-steve'}:
        raise ValueError('Agent fleet changed; review required')
    brad=entries['career-brad']; steve=entries['career-steve']
    if brad.get('model',{}).get('primary')!='openai/gpt-6.1-sol' or brad.get('thinkingDefault')!='medium':
        raise ValueError('Brad baseline changed; review required')
    if steve.get('tools',{}).get('deny')!=['*'] or steve.get('tools',{}).get('elevated',{}).get('enabled') is not False or steve.get('memory',{}).get('search',{}).get('enabled') is not False or steve.get('heartbeat',{}).get('every')!='0m':
        raise ValueError('Steve security boundary changed; review required')
    if steve.get('model',{}).get('primary') not in ['openai/gpt-5.6-sol','openai/gpt-6.1-sol']:
        raise ValueError('Steve model changed; review required')
    steve['model']['primary']='openai/gpt-6.1-sol'; steve['thinkingDefault']='medium'
    return result

def main():
    if pathlib.Path.home()!=pathlib.Path('/home/steve'): raise SystemExit('Run as steve without sudo')
    def command(args,env=None): return subprocess.run(args,capture_output=True,text=True,env=env,timeout=45)
    if command([RUNTIME,'--version']).stdout.strip()!=VERSION: raise SystemExit('Unqualified installed runtime')
    os.umask(0o077)
    config=pathlib.Path('/home/steve/.openclaw/openclaw.json'); before=config.read_text(); proposed=aligned_config(json.loads(before))
    after=json.dumps(proposed,indent=2)+'\n'; validation=config.with_name('career-steve-validation.json')
    validation.write_text(after)
    try:
        if command([RUNTIME,'config','validate'],{**os.environ,'OPENCLAW_CONFIG_PATH':str(validation)}).returncode:
            raise SystemExit('Native schema rejected proposed settings; no change made')
    finally: validation.unlink(missing_ok=True)
    if json.loads(before)==proposed: print('Steve already aligned; no change made.'); return
    if config.read_text()!=before: raise SystemExit('Concurrent configuration change; no change made')
    backup=pathlib.Path('/home/steve/.openclaw-career-backups')/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ-steve')
    backup.mkdir(mode=0o700,parents=True); (backup/'openclaw.json').write_text(before)
    def write(value):
        mode=config.stat().st_mode&0o777; tmp=config.with_name('openclaw.json.steve-alignment')
        tmp.write_text(value); os.chmod(tmp,mode); os.replace(tmp,config)
    write(after)
    try:
        # Native configuration reload owns reconciliation; no unrelated restart or schedule edits.
        deadline=time.monotonic()+180
        while time.monotonic()<deadline:
            time.sleep(3)
            check=command([RUNTIME,'cron','list','--all','--json','--timeout','10000'])
            if not check.returncode:
                if json.loads(config.read_text())!=proposed: raise RuntimeError('Concurrent configuration change')
                break
        else: raise RuntimeError('Gateway control did not recover within startup grace')
    except BaseException:
        if config.read_text()==after: write(before)
        raise SystemExit('Verification failed; scoped rollback attempted. Private backup: '+str(backup))
    print(json.dumps({'steveModel':'openai/gpt-6.1-sol','thinking':'medium','otherConfiguration':'preserved','privateBackup':str(backup),'liveModelTrial':'pending'}))

if __name__=='__main__': main()
