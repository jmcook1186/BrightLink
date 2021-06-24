import pytest
import time
from brownie import (

    interface
)

def check_initial_balances(load_customer):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    assert dai.balanceOf(contract) ==0
    assert adai.balanceOf(contract)==0
    assert dai.balanceOF(load_customer)==0

    return

def test_initial_deposit(set_deposit_amount, getDeployedContract, load_donor, load_owner):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    contract = getDeployedContract

    initialContractBalance = dai.balanceOf(contract)
    initialDonorBalance = dai.balanceOf(load_donor)

    dai.transfer(contract,set_deposit_amount,{'from':load_donor})
    
    time.sleep(2)

    contract.lockDepositBalance({'from':load_owner})

    finalContractBalance = dai.balanceOf(contract)
    finalDonorBalance = dai.balanceOf(load_donor)

    assert set_deposit_amount > 0
    assert finalContractBalance == initialContractBalance + set_deposit_amount
    assert finalDonorBalance == initialDonorBalance - set_deposit_amount

    return


def test_move_funds_to_aave(set_deposit_amount, getDeployedContract, load_owner):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    initialDaiBalance = dai.balanceOf(contract)
    initialAdaiBalance = adai.balanceOf(contract)

    assert initialDaiBalance == set_deposit_amount
    assert initialAdaiBalance == 0
    
    contract.depositFundsToAave({'from':load_owner})

    time.sleep(10)

    finalDaiBalance = dai.balanceOf(contract)
    finalAdaiBalance = adai.balanceOf(contract)

    assert finalDaiBalance == 0
    assert finalAdaiBalance >= set_deposit_amount
    
    return

def test_aave_interest(getDeployedContract):
    
    contract = getDeployedContract
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    t1 = adai.balanceOf(contract)
    time.sleep(20)
    t2 = adai.balanceOf(contract)
    time.sleep(20)
    t3 = adai.balanceOf(contract)

    assert t3 > t2
    assert t2 > t1

    return



def test_withdrawal_from_aave(set_deposit_amount, getDeployedContract, load_owner):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    contract.WithdrawFundsFromAave({'from': load_owner})

    assert dai.balanceOf(contract) >= set_deposit_amount
    assert adai.balanceOf(contract) == 0

    return


def test_send_link(getDeployedContract, load_owner):
    
    nLINK = 0.3e18
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')
    initial_LINK_balance = link.balanceOf(getDeployedContract)
    link.transfer(getDeployedContract,nLINK,{'from':load_owner})
    assert link.balanceOf(getDeployedContract) == initial_LINK_balance + nLINK

    return


def test_oracle_request(getDeployedContract, load_owner):
    
    contract = getDeployedContract

    contract.requestDataFromAPI({'from':load_owner})
    trigger = contract.viewValueFromOracle()
    assert trigger != 0

    return


def test_withdrawal_from_contract(set_deposit_amount, getDeployedContract, load_owner, load_customer, load_donor, set_threshold):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract
    trigger = contract.viewValueFromOracle()

    assert adai.balanceOf(contract) == 0
    assert dai.balanceOf(contract) > set_deposit_amount

    initialOwnerBalance = dai.balanceOf(load_owner)
    initialCustomerBalance = dai.balanceOf(load_customer)
    initialDonorBalance = dai.balanceOf(load_donor)

    contract.retrieveDAI({'from':load_owner})
    
    time.sleep(20)

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

    return

def test_reset_fund_allocation(getDeployedContract, load_owner,load_customer,load_donor):

    contract = getDeployedContract
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')

    if link.balanceOf(contract) > 0:
        contract.retrieveLINK({'from':load_owner})
    
    if dai.balanceOf(contract) > 0:
        contract.escapeHatch({'from':load_owner})
    
    if dai.balanceOf(load_customer) >0:
        dai.transfer(load_donor,dai.balanceOf(load_customer),{'from':load_customer})

    return