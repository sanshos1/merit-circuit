from conftest import CONTRACT
U=['https://work.example/contribution','https://maintainer.example/attestation']
def mocks(v):
 v.strict_mocks=True;v.check_pickling=True;v.mock_web(r'work\.example',{'status':200,'body':'Merged contribution with tests and docs.'});v.mock_web(r'maintainer\.example',{'status':200,'body':'Maintainer confirms production use.'});v.mock_web(r'appeal\.example',{'status':200,'body':'Additional adoption evidence.'});v.mock_llm(r'.*Score documented.*','{"score":85,"components":[{"code":"QUALITY","points":50},{"code":"ADOPTION","points":35}]}');v.mock_llm(r'.*Verify exact score.*','{"valid":true}')
def test_score_appeal(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);mocks(direct_vm);c.open_epoch('E1',c.admin,'SDK work',U);c.score('E1');assert c.get_epoch('E1')['score']==85;c.appeal('E1','https://appeal.example/additional');c.finalize('E1');assert c.get_epoch('E1')['state']=='FINAL'
def test_ids_sources(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);c.open_epoch('A',c.admin,'work',U)
 with direct_vm.expect_revert('duplicate'):c.open_epoch(' a ',c.admin,'work',U)
 with direct_vm.expect_revert('independent'):c.open_epoch('B',c.admin,'work',[U[0],U[0]])
def test_forged_score(direct_vm,direct_deploy):
 c=direct_deploy(CONTRACT);mocks(direct_vm);c.open_epoch('X',c.admin,'work',U);x=c._score(c.epochs['X']);assert direct_vm.run_validator(leader_result=x);x=dict(x);x['score']=84;assert not direct_vm.run_validator(leader_result=x)
