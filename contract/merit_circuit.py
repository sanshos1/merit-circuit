# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
from dataclasses import dataclass
import hashlib,json
def c(v,n=900):return str(v).strip()[:n]
def kid(v):
 x=c(v,72).upper()
 if not x:raise gl.vm.UserError('[EXPECTED] epoch id required')
 return x
def url(v):
 s=c(v,500);r=s[8:] if s.startswith('https://') else '';h=r.split('/')[0].lower();p=r[len(h):]
 if not h or '.' not in h or '@' in h or not p.startswith('/'):raise gl.vm.UserError('[EXPECTED] valid HTTPS source')
 return s,h
def obj(v):
 if isinstance(v,dict):return v
 s=str(v);a=s.find('{');b=s.rfind('}')
 if a<0 or b<=a:raise gl.vm.UserError('[LLM_ERROR] invalid JSON')
 return json.loads(s[a:b+1])
@allow_storage
@dataclass
class Epoch:maintainer:Address;subject:Address;scope:str;sources:str;state:str;score:u256;components:str;digests:str;appeal:str
class MeritCircuit(gl.Contract):
 admin:Address;epochs:TreeMap[str,Epoch]
 def __init__(self):self.admin=gl.message.sender_address
 def _get(self,i):
  k=kid(i)
  if k not in self.epochs:raise gl.vm.UserError('[EXPECTED] epoch not found')
  return k,self.epochs[k]
 @gl.public.write
 def open_epoch(self,i:str,subject:Address,scope:str,sources:list[str])->None:
  k=kid(i)
  if k in self.epochs:raise gl.vm.UserError('[EXPECTED] duplicate epoch id')
  p=[url(x) for x in sources]
  if len(p)!=2 or p[0][1]==p[1][1]:raise gl.vm.UserError('[EXPECTED] two independent source hosts required')
  self.epochs[k]=Epoch(gl.message.sender_address,subject,c(scope,120),json.dumps([x[0] for x in p]),'OPEN',u256(0),'[]','[]','')
 def _score(self,e,appeal=''):
  urls=json.loads(e.sources)+([appeal] if appeal else [])
  def run():
   docs=[];dig=[]
   for ix,u in enumerate(urls):
    raw=gl.nondet.web.get(u).body[:14000];b=raw if isinstance(raw,bytes) else str(raw).encode();dig.append(hashlib.sha256(b).hexdigest());docs.append({'slot':ix,'body':b.decode(errors='replace')})
   q='Score documented contribution merit. JSON only {"score":0,"components":[{"code":"QUALITY","points":0}]}. Component points must sum exactly to score, range 0..100. SCOPE:'+e.scope+' DOCS:'+json.dumps(docs)
   x=obj(gl.nondet.exec_prompt(q,response_format='json'));components=x.get('components',[])[:10];score=max(0,min(100,int(x.get('score',0))));norm=sorted([{'code':c(v.get('code'),40).upper(),'points':max(0,min(100,int(v.get('points',0))))} for v in components if c(v.get('code'),40)],key=lambda z:z['code'])
   if sum(v['points'] for v in norm)!=score:return {'score':0,'components':[],'digests':dig}
   return {'score':score,'components':norm,'digests':dig}
  def valid(x):
   if not isinstance(x,gl.vm.Return):return False
   try:
    g=x.calldata;docs=[];dig=[]
    for ix,u in enumerate(urls):
     raw=gl.nondet.web.get(u).body[:14000];b=raw if isinstance(raw,bytes) else str(raw).encode();dig.append(hashlib.sha256(b).hexdigest());docs.append({'slot':ix,'body':b.decode(errors='replace')})
    if g['digests']!=dig or sum(v['points'] for v in g['components'])!=g['score']:return False
    q='Verify exact score and every component point from the records. JSON only {"valid":true}. PROPOSAL:'+json.dumps(g)+' DOCS:'+json.dumps(docs)
    return bool(obj(gl.nondet.exec_prompt(q,response_format='json')).get('valid',False))
   except:return False
  return gl.vm.run_nondet_unsafe(run,valid)
 @gl.public.write
 def score(self,i:str)->None:
  _,e=self._get(i)
  if e.state!='OPEN':raise gl.vm.UserError('[EXPECTED] scoring unavailable')
  x=self._score(e);e.score=u256(x['score']);e.components=json.dumps(x['components']);e.digests=json.dumps(x['digests']);e.state='SCORED'
 @gl.public.write
 def appeal(self,i:str,evidence:str)->None:
  _,e=self._get(i);u,_=url(evidence)
  if e.subject!=gl.message.sender_address or e.state!='SCORED':raise gl.vm.UserError('[EXPECTED] subject scored epoch required')
  if u in json.loads(e.sources):raise gl.vm.UserError('[EXPECTED] distinct appeal evidence required')
  e.appeal=u;e.state='APPEALED'
 @gl.public.write
 def finalize(self,i:str)->None:
  _,e=self._get(i)
  if e.state=='SCORED':e.state='FINAL';return
  if e.state!='APPEALED':raise gl.vm.UserError('[EXPECTED] finalization unavailable')
  x=self._score(e,e.appeal);e.score=u256(x['score']);e.components=json.dumps(x['components']);e.digests=json.dumps(x['digests']);e.state='FINAL'
 @gl.public.view
 def get_epoch(self,i:str)->dict:
  k,e=self._get(i);return {'id':k,'maintainer':e.maintainer.as_hex,'subject':e.subject.as_hex,'scope':e.scope,'sources':json.loads(e.sources),'state':e.state,'score':int(e.score),'components':json.loads(e.components),'digests':json.loads(e.digests),'appeal':e.appeal}
