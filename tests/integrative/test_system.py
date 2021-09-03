
import pytest
import time
from brownie import (

    interface
)

def test_initial_balances(load_customer, getDeployedContract):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    assert dai.balanceOf(contract) ==0
    assert adai.balanceOf(contract)==0

    return

def test_approvals(load_donor, getDeployedContract, set_deposit_amount):
    
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    dai.approve(getDeployedContract, set_deposit_amount, {'from':load_donor})

    return


def test_system(set_deposit_amount, getDeployedContract, load_owner, load_customer, load_donor):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')

    contract = getDeployedContract

    link.transfer(contract,0.6e18,{'from':load_owner})
    assert link.balanceOf(contract)== 0.6e18

    dai.approve(contract,set_deposit_amount,{'from':load_donor})
    contract.addNewCustomer(load_customer, load_donor, set_deposit_amount, {'from': load_owner})
    

    assert contract.checkIdForCustomer(load_customer)==0
    assert contract.checkvalueForAgreementId(0)==set_deposit_amount
    assert dai.balanceOf(contract) == 0
    assert adai.balanceOf(contract) >= set_deposit_amount
    assert contract.checkBalance()[0] == 0
    assert contract.checkBalance()[1] >= set_deposit_amount



    contract.setBaseLine(load_customer,100,100,100,{'from':load_owner})
    time.sleep(10)
    baseline = contract.viewValueFromOracle() 

    bal = contract.checkBalance()[1]
    contract.takeProfits({'from':load_owner})
    newbal = contract.checkBalance()[1]
    assert bal > newbal
    newbal==set_deposit_amount

    contract.UpdateOracleData(load_customer, 100,100,100, {'from': load_owner})
    time.sleep(10)
    oracleData = contract.viewValueFromOracle()

    print("baseline: ", baseline)
    print("updated data: ", oracleData)

    preSettleBalCust = dai.balanceOf(load_customer)
    preSettleBalDonor = dai.balanceOf(load_donor)
    contract.settleAgreement(load_customer, {'from': load_owner})
    postSettleBalCust = dai.balanceOf(load_customer)
    postSettleBalDonor = dai.balanceOf(load_donor)

    if oracleData > baseline:
        
        assert preSettleBalCust < postSettleBalCust

    else:
        assert preSettleBalDonor < postSettleBalDonor

    # reset wallet balances before next iteration

    if dai.balanceOf(contract) !=0:
        dai.transfer(load_owner,dai.balanceOf(contract),{'from':contract})
    
    if dai.balanceOf(load_customer) !=0:
        dai.transfer(load_donor,dai.balanceOf(load_customer),{'from':load_customer})


    return