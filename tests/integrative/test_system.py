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
    assert dai.balanceOf(load_customer)==0

    return


def test_system(set_deposit_amount, getDeployedContract, load_owner, load_customer, load_donor, set_threshold):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')

    contract = getDeployedContract

    link.transfer(contract,0.3e18,{'from':load_owner})
    assert link.balanceOf(contract)!=0

    dai.transfer(contract,set_deposit_amount,{'from':load_donor})
    assert dai.balanceOf(contract) == set_deposit_amount

    contract.lockDepositBalance({'from':load_owner})
    assert contract.checkBalance()[0] == set_deposit_amount

    contract.depositFundsToAave({'from':load_owner})
    assert dai.balanceOf(contract)==0
    assert adai.balanceOf(contract)!=0

    contract.setWeights(100,100,100,{'from':load_owner})
    
    time.sleep(30)

    contract.requestDataFromAPI({'from':load_owner})
    trigger = contract.viewValueFromOracle()
    assert trigger != 0

    contract.WithdrawFundsFromAave({'from': load_owner})
    assert dai.balanceOf(contract)>set_deposit_amount
    assert adai.balanceOf(contract)==0

    initialOwnerBalance = dai.balanceOf(load_owner)
    initialCustomerBalance = dai.balanceOf(load_customer)
    initialDonorBalance = dai.balanceOf(load_donor)

    contract.retrieveDAI({'from':load_owner})

    if trigger > set_threshold:

        assert adai.balanceOf(contract) == 0
        assert dai.balanceOf(contract) == 0
        assert dai.balanceOf(load_owner) > initialOwnerBalance
        assert dai.balanceOf(load_customer) == initialCustomerBalance+set_deposit_amount
        assert dai.balanceOf(load_donor) == initialDonorBalance
    
    else:
        assert adai.balanceOf(contract) == 0
        assert dai.balanceOf(contract) == 0
        assert dai.balanceOf(load_owner) > initialOwnerBalance
        assert dai.balanceOf(load_customer) == initialCustomerBalance
        assert dai.balanceOf(load_donor) == initialDonorBalance+set_deposit_amount

    # reset wallet balances before next iteration

    if dai.balanceOf(contract) !=0:
        dai.transfer(load_owner,dai.balanceOf(contract),{'from':contract})
    
    if dai.balanceOf(load_customer) !=0:
        dai.transfer(load_donor,dai.balanceOf(load_customer),{'from':load_customer})


    return