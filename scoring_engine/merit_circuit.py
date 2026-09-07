# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
from datetime import datetime,timezone
from urllib.parse import urlsplit,unquote
import hashlib,json
def c(v,n=900):return str(v).strip()[:n]
def kid(v):
 x=c(v,72).upper()
 if not x:raise gl.vm.UserError('[EXPECTED] epoch id required')
 return x
def url(v):
 s=c(v,500);p=urlsplit(s)
 if p.scheme.lower()!='https' or not p.hostname or p.username or p.password or p.fragment:raise gl.vm.UserError('[EXPECTED] valid HTTPS source')
 host=p.hostname.lower().rstrip('.');path=unquote(p.path or '/')
 if any(x in ('.','..') for x in path.split('/')):raise gl.vm.UserError('[EXPECTED] normalized HTTPS source')
 return s,host
def obj(v):
 if isinstance(v,dict):return v
 s=str(v);a=s.find('{');b=s.rfind('}')
 if a<0 or b<=a:raise gl.vm.UserError('[LLM_ERROR] invalid JSON')
 return json.loads(s[a:b+1])
@allow_storage
@dataclass
class Epoch:maintainer:Address;subject:str;scope:str;sources:str;appeal_deadline:u256;state:str;score:u256;components:str;digests:str;appeal:str
class MeritCircuit(gl.Contract):
 admin:Address;epochs:TreeMap[str,Epoch]
 def __init__(self):self.admin=gl.message.sender_address
 def _get(self,i):
  k=kid(i)
  if k not in self.epochs:raise gl.vm.UserError('[EXPECTED] epoch not found')
  return k,self.epochs[k]
 @gl.public.write
 def open_epoch(self,i:str,subject:str,scope:str,sources:list[str],appeal_deadline:u256)->None:
  k=kid(i);p=[url(x) for x in sources];deadline=int(appeal_deadline);now=int(datetime.now(timezone.utc).timestamp())
  if k in self.epochs:raise gl.vm.UserError('[EXPECTED] duplicate epoch id')
  if len(p)!=2 or p[0][1]==p[1][1]:raise gl.vm.UserError('[EXPECTED] two independent source hosts required')
  if deadline<=now:raise gl.vm.UserError('[EXPECTED] future appeal deadline required')
  self.epochs[k]=Epoch(gl.message.sender_address,c(subject,42).lower(),c(scope,120),json.dumps([x[0] for x in p]),u256(deadline),'OPEN',u256(0),'[]','[]','')
 def _score(self,e,appeal=''):
  urls=json.loads(e.sources)+([appeal] if appeal else [])
  def run():
   docs=[];dig=[]
   for ix,u in enumerate(urls):
    response=gl.nondet.web.get(u)
    if response.status!=200:raise gl.vm.UserError('[EXTERNAL] evidence unavailable')
    raw=response.body;b=raw if isinstance(raw,bytes) else str(raw).encode();dig.append(hashlib.sha256(b).hexdigest());docs.append({'slot':ix,'body':b.decode(errors='replace')[:14000]})
   q='Apply immutable rubric QUALITY 0..60 plus ADOPTION 0..40. JSON only {"score":0,"components":[{"code":"QUALITY","points":0},{"code":"ADOPTION","points":0}]}. Both required and sum to score. SCOPE:'+e.scope+' DOCS:'+json.dumps(docs)
   x=obj(gl.nondet.exec_prompt(q,response_format='json'));norm=sorted([{'code':c(v.get('code'),40).upper(),'points':int(v.get('points',-1))} for v in x.get('components',[])],key=lambda z:z['code']);score=int(x.get('score',-1))
   if [v['code'] for v in norm]!=['ADOPTION','QUALITY'] or not 0<=norm[0]['points']<=40 or not 0<=norm[1]['points']<=60 or score!=sum(v['points'] for v in norm):raise gl.vm.UserError('[LLM_ERROR] invalid rubric result')
   return {'score':score,'components':norm,'digests':dig}
  def valid(x):
   if not isinstance(x,gl.vm.Return):return False
   try:
    g=x.calldata;docs=[];dig=[]
    for ix,u in enumerate(urls):
     response=gl.nondet.web.get(u)
     if response.status!=200:return False
     raw=response.body;b=raw if isinstance(raw,bytes) else str(raw).encode();dig.append(hashlib.sha256(b).hexdigest());docs.append({'slot':ix,'body':b.decode(errors='replace')[:14000]})
    parts=g.get('components',[])
    if g['digests']!=dig or len(parts)!=2 or sorted(v.get('code') for v in parts)!=['ADOPTION','QUALITY'] or sum(int(v.get('points',-1)) for v in parts)!=int(g.get('score',-1)):return False
    caps={v['code']:int(v['points']) for v in parts}
    if not 0<=caps['QUALITY']<=60 or not 0<=caps['ADOPTION']<=40:return False
    q='Recompute and verify exact QUALITY points, ADOPTION points, and total under caps 60 and 40. JSON only {"valid":true}. PROPOSAL:'+json.dumps(g)+' DOCS:'+json.dumps(docs)
    return bool(obj(gl.nondet.exec_prompt(q,response_format='json')).get('valid',False))
   except:return False
  return gl.vm.run_nondet_unsafe(run,valid)
 @gl.public.write
 def score(self,i:str)->None:
  _,e=self._get(i)
  if e.state!='OPEN':raise gl.vm.UserError('[EXPECTED] scoring unavailable')
  x=self._score(e);e.score=u256(x['score']);e.components=json.dumps(x['components']);e.digests=json.dumps(x['digests']);e.state='APPEAL_OPEN'
 @gl.public.write
 def appeal(self,i:str,evidence:str)->None:
  _,e=self._get(i);u,h=url(evidence);now=int(datetime.now(timezone.utc).timestamp())
  if e.subject!=gl.message.sender_address.as_hex.lower() or e.state!='APPEAL_OPEN' or now>int(e.appeal_deadline):raise gl.vm.UserError('[EXPECTED] subject appeal window required')
  if h in [url(x)[1] for x in json.loads(e.sources)]:raise gl.vm.UserError('[EXPECTED] independent appeal host required')
  e.appeal=u;e.state='APPEALED'
 @gl.public.write
 def finalize(self,i:str)->None:
  _,e=self._get(i)
  if e.state not in ('APPEAL_OPEN','APPEALED') or int(datetime.now(timezone.utc).timestamp())<=int(e.appeal_deadline):raise gl.vm.UserError('[EXPECTED] appeal window still open')
  if e.state=='APPEALED':
   x=self._score(e,e.appeal);e.score=u256(x['score']);e.components=json.dumps(x['components']);e.digests=json.dumps(x['digests'])
  e.state='FINAL'
 @gl.public.view
 def get_epoch(self,i:str)->dict:
  k,e=self._get(i);return {'id':k,'maintainer':e.maintainer.as_hex,'subject':e.subject,'scope':e.scope,'sources':json.loads(e.sources),'appealDeadline':int(e.appeal_deadline),'state':e.state,'score':int(e.score),'components':json.loads(e.components),'digests':json.loads(e.digests),'appeal':e.appeal}
