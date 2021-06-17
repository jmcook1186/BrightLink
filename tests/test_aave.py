
import pytest
import time
from brownie import (

    interface
)

def check_initial_balances():

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    assert dai.balanceOf(contract) ==0
    assert adai.balanceOf(contract)==0

    return

def test_initial_deposit(set_deposit_amount, getDeployedContract, load_account):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    contract = getDeployedContract

    initialBalance = dai.balanceOf(contract)
    dai.transfer(contract,set_deposit_amount,{'from':load_account})
    
    time.sleep(10)
    finalBalance = dai.balanceOf(contract)

    assert set_deposit_amount > 0
    assert finalBalance == initialBalance + set_deposit_amount

    return


def test_move_funds_to_aave(set_deposit_amount, getDeployedContract, load_account):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    initialDaiBalance = dai.balanceOf(contract)
    initialAdaiBalance = adai.balanceOf(contract)

    assert initialDaiBalance == set_deposit_amount
    assert initialAdaiBalance == 0
    
    contract.depositFundsToAave({'from':load_account})

    time.sleep(10)

    finalDaiBalance = dai.balanceOf(contract)
    finalAdaiBalance = adai.balanceOf(contract)

    assert finalDaiBalance == 0
    assert finalAdaiBalance >= set_deposit_amount
    
    return

def test_profit(set_deposit_amount, getDeployedContract):

    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    assert adai.balanceOf(contract) > set_deposit_amount

    return

def test_withdrawal_from_aave(set_deposit_amount, getDeployedContract, load_account):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    contract.WithdrawFundsFromAave({'from': load_account})

    assert dai.balanceOf(contract) >= set_deposit_amount
    assert adai.balanceOf(contract) == 0

    return

def test_withdrawal_from_contract(set_deposit_amount, getDeployedContract, load_account):

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    initialBalance = dai.balanceOf(load_account)
    initialContractBalance = dai.balanceOf(contract)

    contract.retrieveDAI({'from':load_account})
    time.sleep(10)

    assert dai.balanceOf(contract) == 0
    assert adai.balanceOf(contract) == 0
    assert adai.balanceOf(load_account) == 0
    assert dai.balanceOf(load_account) == (initialBalance + initialContractBalance)

    return