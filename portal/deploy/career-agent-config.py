#!/usr/bin/env python3
"""Pure config transformation. Existing provider secrets and personal routing remain intact."""
import copy

def career_config(original,workspace_base):
 config=copy.deepcopy(original)
 entries=config.setdefault('agents',{}).setdefault('entries',{})
 if 'main' not in entries or set(entries)-{'main','career-brad','career-steve'}:raise ValueError('Review required: unrecognized agent fleet')
 primary=config['agents']['defaults']['model']['primary']
 if not primary.startswith('openai/'):raise ValueError('Subscription primary changed; review required')
 for candidate in ['brad','steve']:
  if 'career-'+candidate in entries:
   existing=entries['career-'+candidate]
   if existing.get('tools',{}).get('deny')!=['*'] or existing.get('tools',{}).get('elevated',{}).get('enabled') is not False or existing.get('memory',{}).get('search',{}).get('enabled') is not False or existing.get('heartbeat',{}).get('every')!='0m':raise ValueError('Existing career policy changed; review required')
   continue
  entries['career-'+candidate]={'name':candidate.title()+' career assistant','workspace':str(workspace_base+'/'+candidate),'model':{'primary':primary,'fallbacks':copy.deepcopy(config['agents']['defaults']['model'].get('fallbacks',[]))},'utilityModel':'','memory':{'search':{'enabled':False,'rememberAcrossConversations':False}},'heartbeat':{'every':'0m'},'skills':[],'tools':{'profile':'minimal','deny':['*'],'elevated':{'enabled':False}},'subagents':{'allowAgents':[]}}
 # Making an implicit sole-agent fleet explicit requires retaining its ambient owner routes.
 config['agents']['ownership']='explicit'
 defaults=config['agents']['defaults'];defaults.setdefault('heartbeat',{})['agentId']='main';defaults.setdefault('systemAgent',{})['agentId']='main'
 bindings=config.setdefault('bindings',[])
 for channel in config.get('channels',{}):
  if not any(b.get('match',{}).get('channel')==channel and b.get('match',{}).get('accountId')=='*' for b in bindings):bindings.append({'agentId':'main','match':{'channel':channel,'accountId':'*'}})
 config.setdefault('talk',{})['agentId']='main'
 config.setdefault('gateway',{}).setdefault('http',{}).setdefault('endpoints',{})['chatCompletions']={'enabled':True,'images':{'allowUrl':False}}
 return config
