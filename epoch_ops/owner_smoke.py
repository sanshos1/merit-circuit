"""Owner-only replacement deployment check. No other account keys are loaded."""
import json,base64,hashlib,time
from pathlib import Path
from genlayer_py import create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus
from owner_wallet import owner_account
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'evidence/deployment.json').read_text())
account=owner_account()
assert d['deployer'].lower()==account.address.lower()
client=create_client(chain=studionet,account=account)
path=ROOT/'evidence/owner-network.json'
out=json.loads(path.read_text()) if path.exists() else {'contract':d['contract'],'wallet':account.address,'network':'StudioNet','transactions':{}}
assert out['contract']==d['contract']
def save(): path.write_text(json.dumps(out,indent=2)+'\n')
receipt=client.get_transaction(transaction_hash=d['deploymentTx'])
raw=base64.b64decode(receipt['data']['contract_code'],validate=True)
assert raw==(ROOT/'scoring_engine/merit_circuit.py').read_text(encoding='utf-8').encode()
assert receipt['recipient'].lower()==d['contract'].lower()
out['sourceMatches']=True
out['sourceSha256']=hashlib.sha256(raw).hexdigest()
out['deploymentStatus']=receipt['status_name']
out['deploymentTx']=d['deploymentTx']
save()
def send(label,method,args):
    entry=out['transactions'].get(label,{})
    if not entry.get('hash'):
        entry={'hash':client.write_contract(address=d['contract'],function_name=method,args=args)}
        out['transactions'][label]=entry;save()
    print(label,entry['hash'],flush=True)
    client.wait_for_transaction_receipt(transaction_hash=entry['hash'],status=TransactionStatus.ACCEPTED,retries=120,interval=5000)
    info=client.get_transaction(transaction_hash=entry['hash'])
    if not any(r.get('execution_result')=='SUCCESS' for r in info.get('consensus_data',{}).get('leader_receipt',[])):
        raise RuntimeError('Execution failure: '+label)
    if info['from_address'].lower()!=account.address.lower(): raise RuntimeError('Unexpected signer')
    entry.update({'status':info['status_name'],'execution':'SUCCESS','signer':account.address});save()
out.setdefault('id','MC-OWNER-'+str(int(time.time())))
out.setdefault('requestedDeadline',int(time.time())+60);save()
sources=['https://raw.githubusercontent.com/sanshos1/merit-circuit/c97f9a6d5278d265e71c56db227527826a82f8de/evidence/contribution.txt','https://cdn.jsdelivr.net/gh/sanshos1/merit-circuit@c97f9a6d5278d265e71c56db227527826a82f8de/evidence/attestation.txt']
send('open','open_epoch',[out['id'],account.address,'Owner-only SDK contribution test',sources,out['requestedDeadline']])
send('score','score',[out['id']])
send('appeal','appeal',[out['id'],'https://github.com/sanshos1/merit-circuit/raw/c97f9a6d5278d265e71c56db227527826a82f8de/evidence/appeal.txt'])
state=client.read_contract(address=d['contract'],function_name='get_epoch',args=[out['id']])
if int(time.time())>state['appealDeadline'] and state['state']!='FINAL':
    send('finalize','finalize',[out['id']])
    state=client.read_contract(address=d['contract'],function_name='get_epoch',args=[out['id']])
out['state']=state
out['pendingFinalization']=state['state']!='FINAL'
save()
print(json.dumps(out,indent=2),flush=True)
