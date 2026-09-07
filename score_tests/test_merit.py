from conftest import CONTRACT
from datetime import datetime,timezone
U=['https://work.example/contribution','https://maintainer.example/attestation']
def now():return int(datetime.now(timezone.utc).timestamp())
def mocks(v):
 v.strict_mocks=True;v.check_pickling=True;v.mock_web(r'work\.example',{'status':200,'body':'Merged contribution with tests and docs.'});v.mock_web(r'maintainer\.example',{'status':200,'body':'Independent maintainer confirms production use.'});v.mock_web(r'appeal\.example',{'status':200,'body':'Additional adoption evidence.'});v.mock_llm(r'.*immutable rubric.*','{"score":85,"components":[{"code":"QUALITY","points":50},{"code":"ADOPTION","points":35}]}');v.mock_llm(r'.*Recompute and verify.*','{"valid":true}')
def test_score_opens_enforceable_appeal_window(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);mocks(direct_vm);c.open_epoch('E1',c.admin.as_hex,'SDK work',U,now()+100);c.score('E1');assert c.get_epoch('E1')['state']=='APPEAL_OPEN'
 with direct_vm.expect_revert('still open'):c.finalize('E1')
 c.appeal('E1','https://appeal.example/additional');assert c.get_epoch('E1')['state']=='APPEALED'
def test_sources_configurable_and_distinct(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);c.open_epoch('A',c.admin.as_hex,'work',U,now()+100);assert c.get_epoch('A')['sources']==U
 with direct_vm.expect_revert('duplicate'):c.open_epoch(' a ',c.admin.as_hex,'work',U,now()+100)
 with direct_vm.expect_revert('independent'):c.open_epoch('B',c.admin.as_hex,'work',[U[0],U[0]],now()+100)
def test_rubric_caps_reject_bad_result(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);c.open_epoch('R',c.admin.as_hex,'work',U,now()+100);direct_vm.strict_mocks=True;direct_vm.mock_web(r'work\.example',{'status':200,'body':'work'});direct_vm.mock_web(r'maintainer\.example',{'status':200,'body':'use'});direct_vm.mock_llm(r'.*immutable rubric.*','{"score":100,"components":[{"code":"QUALITY","points":80},{"code":"ADOPTION","points":20}]}')
 with direct_vm.expect_revert('invalid rubric'):c.score('R')
def test_forged_component_rejected(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);mocks(direct_vm);c.open_epoch('X',c.admin.as_hex,'work',U,now()+100);x=c._score(c.epochs['X']);assert direct_vm.run_validator(leader_result=x);x=dict(x);x['components'][0]['points']=34;assert not direct_vm.run_validator(leader_result=x)
