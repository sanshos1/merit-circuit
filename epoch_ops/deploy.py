"""Deploy the reviewed source with the project owner's wallet only."""
import json, hashlib, subprocess
from pathlib import Path
from genlayer_py import create_client
from genlayer_py.chains import studionet
from genlayer_py.types import TransactionStatus
from owner_wallet import owner_account
ROOT = Path(__file__).resolve().parents[1]
def main():
    account = owner_account()
    client = create_client(chain=studionet, account=account)
    source = 'scoring_engine/merit_circuit.py'
    code = (ROOT / source).read_text(encoding='utf-8')
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    pending = ROOT / 'evidence/owner-deployment-pending.json'
    if pending.exists():
        job = json.loads(pending.read_text())
        if job['sourceSha256'] != hashlib.sha256(code.encode()).hexdigest():
            raise RuntimeError('Pending deployment source mismatch')
        tx = job['deploymentTx']
    else:
        tx = client.deploy_contract(code=code,args=[])
        pending.write_text(json.dumps({'deploymentTx':tx,'sourceSha256':hashlib.sha256(code.encode()).hexdigest(),'sourceCommit':commit},indent=2))
    print('Owner deployment transaction:',tx,flush=True)
    client.wait_for_transaction_receipt(transaction_hash=tx,status=TransactionStatus.ACCEPTED,retries=120,interval=5000)
    info = client.get_transaction(transaction_hash=tx)
    if not any(r.get('execution_result')=='SUCCESS' for r in info.get('consensus_data',{}).get('leader_receipt',[])):
        raise RuntimeError('Deployment execution did not succeed')
    contract = info['data']['contract_address']
    result = {'contract':contract,'deploymentTx':tx,'network':'StudioNet','deployer':account.address,'sourceCommit':json.loads(pending.read_text())['sourceCommit'],'sourceSha256':hashlib.sha256(code.encode()).hexdigest(),'receiptStatus':info['status_name'],'execution':'SUCCESS','walletPolicy':'ACCOUNT_3 only'}
    (ROOT/'evidence/deployment.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__': main()
