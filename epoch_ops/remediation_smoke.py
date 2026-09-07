import json,re,time,hashlib,subprocess
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus
ROOT=Path(__file__).parents[1]
ENV=(ROOT.parents[3]/'accounts.env').read_text()
D=json.loads((ROOT/'evidence/deployment.json').read_text())
def val(n):return re.search(rf'^{n}\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip()
accounts={i:create_account(account_private_key=val(f'ACCOUNT_{i}_GENLAYER_PRIVATE_KEY')) for i in (1,2,3,4)}
clients={i:create_client(chain=studionet,account=a) for i,a in accounts.items()}
address=D['contract'];commit=D['sourceCommit']
out={'contract':address,'sourceCommit':commit,'network':'StudioNet','transactions':{},'checks':{},'demo':'All role wallets are operator-controlled test accounts, not independent organizations.'}
path=ROOT/'evidence/remediation-network.json'
if path.exists():
 previous=json.loads(path.read_text())
 if previous.get('contract')==address:out=previous
def save():path.write_text(json.dumps(out,indent=2))
def send(client,label,name,args):
 if label in out['transactions']:return out['transactions'][label]
 h=client.write_contract(address=address,function_name=name,args=args);print(label,h,flush=True)
 client.wait_for_transaction_receipt(transaction_hash=h,status=TransactionStatus.ACCEPTED,retries=120,interval=5000)
 info=client.get_transaction(transaction_hash=h)
 success=any(r.get('execution_result')=='SUCCESS' for r in info.get('consensus_data',{}).get('leader_receipt',[]))
 if not success:raise RuntimeError({'tx':h,'status':info.get('status_name'),'result':info.get('tx_execution_result_name')})
 out['transactions'][label]=h;save();return h
def reject(client,label,name,args,message):
 if label in out['checks'] and out['checks'][label].get('verified'):return
 h=out['checks'].get(label,{}).get('tx')
 if not h:
  h=client.write_contract(address=address,function_name=name,args=args);out['checks'][label]={'tx':h};save();print(label,h,flush=True)
 client.wait_for_transaction_receipt(transaction_hash=h,status=TransactionStatus.ACCEPTED,retries=120,interval=5000)
 info=client.get_transaction(transaction_hash=h)
 (ROOT/('evidence/rejection-'+label+'.json')).write_text(json.dumps(info,indent=2,default=str))
 if any(r.get('execution_result')=='SUCCESS' for r in info.get('consensus_data',{}).get('leader_receipt',[])):raise AssertionError('Unexpected success: '+label)
 raw=json.dumps(info,default=str)
 if message not in raw:raise RuntimeError('Inspect recorded rejection receipt: '+label)
 out['checks'][label]={'tx':h,'expectedRejection':message,'verified':True};save()

eid=out.setdefault('id','MC-'+str(int(time.time())));save()
sources=[f'https://raw.githubusercontent.com/sanshos1/merit-circuit/{commit}/evidence/contribution.txt',f'https://cdn.jsdelivr.net/gh/sanshos1/merit-circuit@{commit}/evidence/attestation.txt']
if 'open' not in out['transactions']:
 out['creationDeadline']=int(time.time())+30;save()
send(clients[3],'open','open_epoch',[eid,accounts[4].address,'GenLayer SDK contribution',sources,out['creationDeadline']])
while int(time.time())<=out['creationDeadline']:time.sleep(1)
send(clients[3],'score','score',[eid])
state=clients[3].read_contract(address=address,function_name='get_epoch',args=[eid])
out['state']=state;save()
assert state['appealDeadline']>out['creationDeadline']+86400
if state['state']=='APPEAL_OPEN':
 reject(clients[3],'earlyFinalize','finalize',[eid],'appeal window still open')
 reject(clients[3],'wrongSubject','appeal',[eid,'https://github.com/sanshos1/merit-circuit/raw/'+commit+'/evidence/appeal.txt'],'subject appeal window required')
 send(clients[4],'appeal','appeal',[eid,'https://github.com/sanshos1/merit-circuit/raw/'+commit+'/evidence/appeal.txt'])
state=clients[3].read_contract(address=address,function_name='get_epoch',args=[eid])
if int(time.time())>state['appealDeadline'] and state['state']!='FINAL':
 send(clients[3],'finalize','finalize',[eid])
 state=clients[3].read_contract(address=address,function_name='get_epoch',args=[eid])
out['state']=state;out['pendingFinalization']=state['state']!='FINAL';save()
print(json.dumps(out,indent=2))
