import json,re,time
from pathlib import Path
from genlayer_py import create_client,create_account
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus
ROOT=Path(__file__).parents[1];ENV=(ROOT.parents[3]/'accounts.env').read_text();D=json.loads((ROOT/'evidence/deployment.json').read_text())
def val(n):return re.search(rf'^{n}\s*=\s*"?([^"\r\n]+)',ENV,re.M).group(1).strip()
accounts=[create_account(account_private_key=val(f'ACCOUNT_{i}_GENLAYER_PRIVATE_KEY')) for i in (3,4)];clients=[create_client(chain=studionet,account=a) for a in accounts];address=D['contract'];commit=D['sourceCommit'];eid=f'MC-{int(time.time())}'
sources=[f'https://raw.githubusercontent.com/sanshos1/merit-circuit/{commit}/evidence/contribution.txt',f'https://cdn.jsdelivr.net/gh/sanshos1/merit-circuit@{commit}/evidence/attestation.txt']
def send(client,name,args):
 h=client.write_contract(address=address,function_name=name,args=args);print(name,h,flush=True);client.wait_for_transaction_receipt(transaction_hash=h,status=TransactionStatus.ACCEPTED,retries=120,interval=10000);info=client.get_transaction(transaction_hash=h)
 if info.get('status_name')!='ACCEPTED':raise RuntimeError(info)
 return h
deadline=int(time.time())+90;tx={'open':send(clients[0],'open_epoch',[eid,accounts[1].address,'GenLayer SDK contribution',sources,deadline]),'score':send(clients[0],'score',[eid])}
try:clients[0].simulate_write_contract(address=address,function_name='finalize',args=[eid]);raise RuntimeError('early finalize unexpectedly succeeded')
except Exception:pass
tx['appeal']=send(clients[1],'appeal',[eid,f'https://github.com/sanshos1/merit-circuit/raw/{commit}/evidence/appeal.txt'])
time.sleep(max(0,deadline-int(time.time())+2));tx['finalize']=send(clients[0],'finalize',[eid]);state=clients[0].read_contract(address=address,function_name='get_epoch',args=[eid])
if state['state']!='FINAL' or state['components']!=[{'code':'ADOPTION','points':35},{'code':'QUALITY','points':50}]:raise RuntimeError(state)
(ROOT/'evidence/network-run.json').write_text(json.dumps({'id':eid,'contract':address,'sourceCommit':commit,'earlyFinalizeRejected':True,'transactions':tx,'state':state},indent=2));print(json.dumps(state,indent=2))
