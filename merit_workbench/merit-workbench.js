import { createAccount, createClient } from 'https://esm.sh/genlayer-js@1.1.8';
import { studionet } from 'https://esm.sh/genlayer-js@1.1.8/chains';
const ADDRESS='0x6ce153FD0882Dc74b6425f11A808ba2b100Ba74b', ENDPOINT='https://studio.genlayer.com/api';
let wallet,account;
const reader=createClient({chain:studionet,endpoint:ENDPOINT,account:createAccount()});
const root=document.createElement('main'); root.className='review-sheet';
root.innerHTML=`<style>
*{box-sizing:border-box}body{margin:0;background:#d8d4cb;color:#141414;font:16px Arial,sans-serif}
.review-sheet{display:block;width:min(1180px,calc(100% - 36px));margin:18px auto;padding:0;background:#f7f4ea;min-height:calc(100vh - 36px);border:1px solid #141414;box-shadow:10px 10px 0 #141414}
.mast{display:grid;grid-template-columns:170px 1fr auto;border-bottom:3px solid #141414}.mast>*{padding:22px;border-right:1px solid #141414}.mast>*:last-child{border:0}
.serial{font:700 13px ui-monospace,monospace;letter-spacing:.12em}h1{margin:0;font:900 clamp(2rem,5vw,4.5rem)/.9 Arial,sans-serif;letter-spacing:-.06em}
.badge{align-self:center;background:#2457ff;color:#fff;padding:13px 18px;font-weight:900;transform:rotate(2deg)}
.workspace{display:grid;grid-template-columns:minmax(0,1.65fr) minmax(280px,.75fr)}.worksheet{padding:30px;border-right:3px solid #141414}
.step{display:grid;grid-template-columns:56px 1fr;border-top:1px solid #141414;padding:20px 0}.step-no{font:900 28px ui-monospace,monospace;color:#2457ff}
.fields{display:grid;grid-template-columns:1fr 1fr;gap:14px}label{display:grid;gap:7px;font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.05em}
input{width:100%;border:1px solid #141414;background:#fffef8;padding:13px;font:inherit}.wide{grid-column:1/-1}
.formula{display:grid;grid-template-columns:1fr 1fr;gap:10px}.factor{background:#ffe15a;border:1px solid #141414;padding:15px}.factor b{display:block;font-size:32px}
.actions{display:grid;grid-template-columns:1fr 1fr;gap:9px}button{border:1px solid #141414;background:#fffef8;color:#141414;padding:14px;font-weight:900;text-align:left;cursor:pointer}button:hover,button:focus-visible{background:#2457ff;color:#fff}
.sidebar{display:flex;flex-direction:column}.scorecard{padding:30px;background:#141414;color:#fff}.scorecard small{letter-spacing:.16em}.score-number{font:900 110px/1 Arial,sans-serif;color:#ffe15a}
.ledger{padding:25px;display:grid;gap:16px}.ledger-row{display:grid;grid-template-columns:1fr 80px;border-bottom:1px solid #141414;padding-bottom:10px}.ledger-row span:last-child{text-align:right;font-weight:900}
.status{margin-top:auto;padding:22px;background:#2457ff;color:#fff;font:15px/1.5 ui-monospace,monospace;white-space:pre-wrap;min-height:110px}
@media(max-width:760px){.mast{grid-template-columns:1fr}.mast>*{border-right:0;border-bottom:1px solid #141414}.workspace{grid-template-columns:1fr}.worksheet{border-right:0;border-bottom:3px solid #141414}.fields,.formula,.actions{grid-template-columns:1fr}.wide{grid-column:auto}.step{grid-template-columns:42px 1fr}.score-number{font-size:76px}}
</style>
<header class="mast"><div class="serial">MERIT OFFICE<br>FORM 08</div><div><h1>Contribution<br>review sheet</h1></div><div class="badge">EPOCH OPEN</div></header>
<div class="workspace"><section class="worksheet">
<div class="step"><div class="step-no">01</div><div class="fields"><label>Epoch reference<input id="id" placeholder="Enter a unique epoch reference"></label><label>Subject address<input id="subject" placeholder="0x..."></label><label class="wide">Contribution under review<input id="scope" placeholder="Describe the contribution under review"></label></div></div>
<div class="step"><div class="step-no">02</div><div><div class="formula"><div class="factor">QUALITY EVIDENCE<b>60</b></div><div class="factor">ADOPTION EVIDENCE<b>40</b></div></div><div class="fields"><label>Quality source URL<input id="source1" placeholder="https://..."></label><label>Adoption source URL<input id="source2" placeholder="https://..."></label><label class="wide">Appeal deadline<input id="deadline" type="datetime-local"></label></div><p>Both independent records and the appeal deadline are fixed to this epoch before scoring.</p></div></div>
<div class="step"><div class="step-no">03</div><div class="fields"><label class="wide">Appeal record, only when disputed<input id="appeal" placeholder="https://independent-record.example/review"></label></div></div>
<div class="actions"><button id="open">01 - REGISTER EPOCH</button><button id="scoreBtn">02 - ISSUE SCORE</button><button id="appealBtn">03 - FILE APPEAL</button><button id="finalize">04 - SEAL LEDGER</button></div>
</section><aside class="sidebar"><div class="scorecard"><small>CANONICAL SCORE</small><div class="score-number" id="score">--</div><div>points / 100</div></div>
<div class="ledger"><b>REVIEW LEDGER</b><div class="ledger-row"><span>Source independence</span><span>2 / 2</span></div><div class="ledger-row"><span>Weight equation</span><span>100</span></div><div class="ledger-row"><span>Appeal window</span><span>OPEN</span></div></div>
<output class="status" id="state">Review sheet ready.</output></aside></div>`;
document.body.replaceChildren(root);
const q=s=>root.querySelector(s), value=id=>q('#'+id).value.trim();
const show=x=>{q('#state').textContent=typeof x==='string'?x:JSON.stringify(x,(_,item)=>typeof item==='bigint'?item.toString():item,2)};
async function connect(){const provider=window.ethereum;if(!provider)throw Error('Install MetaMask or Rabby.');[account]=await provider.request({method:'eth_requestAccounts'});if(String(await provider.request({method:'eth_chainId'})).toLowerCase()!=='0xf22f')await provider.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xf22f'}]});wallet=createClient({chain:studionet,endpoint:ENDPOINT,account,provider});if(!value('subject'))q('#subject').value=account;show('Subject wallet connected to StudioNet.')}
async function load(){const result=await reader.readContract({address:ADDRESS,functionName:'get_epoch',args:[value('id')]});show(result);return result}
async function act(functionName,args){try{if(!wallet)await connect();show('Approval requested for '+functionName+'.');const hash=await wallet.writeContract({address:ADDRESS,functionName,args,value:0n});show('Submitted '+hash+'. Waiting for validator acceptance...');await wallet.waitForTransactionReceipt({hash,status:'ACCEPTED',retries:120,interval:5000});show('Accepted. Loading the canonical review ledger...');await load()}catch(error){show(error.message||String(error))}}
q('#open').onclick=()=>act('open_epoch',[value('id'),value('subject'),value('scope'),[value('source1'),value('source2')],Math.floor(new Date(value('deadline')).getTime()/1000)]);
q('#scoreBtn').onclick=async()=>{await act('score',[value('id')]);const state=await load();q('#score').textContent=state.score??'--'};
q('#appealBtn').onclick=()=>act('appeal',[value('id'),value('appeal')]);
q('#finalize').onclick=()=>act('finalize',[value('id')]);
