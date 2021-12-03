"""
Unit tests that cover all functions
in BrightLink v.01

For most functions, security is tested
by attempting to call functions from 
multiple wallets. Expected pass/fail
depends on function's access modifier.

pytest should pick up 17 items

"""

import pytest
import time
from brownie import (

    interface
)


def test_approve_spending(load_customer, load_donor, load_owner, set_deposit_amount, get_deployed_contract):
    """
    make sure all accounts are pre-approved to spend dai
    """
    
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    contract = get_deployed_contract

    dai.approve(contract, set_deposit_amount*10, {'from':load_owner})
    dai.approve(contract, set_deposit_amount*10, {'from': load_donor})
    dai.approve(contract, set_deposit_amount*10, {'from': load_customer})


    return


def test_initial_balances(load_customer, load_donor, load_owner, get_deployed_contract):
    """
    
    ensure contract and customer wallets are empty of DAI at start of testing
    ensures owner's 'escapeHatch' function for retrieving stuck funds works ok

    """
    
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = get_deployed_contract
    contract.escapeHatch({'from':load_owner})
    
    if dai.balanceOf(load_customer)>0:
        dai.transfer(load_donor,dai.balanceOf(load_customer),{'from':load_customer})

    assert dai.balanceOf(contract) ==0
    assert adai.balanceOf(contract)==0
    assert dai.balanceOf(load_customer)==0

    return



def test_add_new_customer(set_deposit_amount, get_deployed_contract, load_customer, load_donor, load_owner):

    
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    contract = get_deployed_contract
    dai.approve(contract, set_deposit_amount*1.5, {'from':load_donor})
    
    initialContractBalance = dai.balanceOf(contract)
    initialDonorBalance = dai.balanceOf(load_donor)

    # make sure donor has enough dai to make the transfer, if not borrow it
    # from owner
    if initialDonorBalance < set_deposit_amount:
        dai.transfer(load_donor,set_deposit_amount,{'from':load_owner})

    contract = get_deployed_contract

    contract.addNewCustomer(load_customer, load_donor, set_deposit_amount, {'from': load_owner})

    finalDonorBalance = dai.balanceOf(load_donor)

    assert (finalDonorBalance < initialDonorBalance)

    return



def test_aave_interest(get_deployed_contract):
    
    """
    ensure funds in aave pool are accruing interest in
    the form of aDAI tokens in the contract
    """

    contract = get_deployed_contract
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    
    t1 = adai.balanceOf(contract)
    time.sleep(20)
    t2 = adai.balanceOf(contract)
    time.sleep(20)
    t3 = adai.balanceOf(contract)

    assert t3 > t2
    assert t2 > t1

    return




def test_send_link(get_deployed_contract, load_owner):
    
    """
    ensure contract receives LINK token to use as oracle gas
    """

    nLINK = 5e18
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')
    initial_LINK_balance = link.balanceOf(get_deployed_contract)
    link.transfer(get_deployed_contract,nLINK,{'from':load_owner})
    assert link.balanceOf(get_deployed_contract) == initial_LINK_balance + nLINK

    return


def test_oracle(set_deposit_amount, get_deployed_contract, load_customer, load_donor, load_owner):
    """
    check the contract calls successfully trigger a chainlink oracle request
    """    
    contract = get_deployed_contract
    
    contract.setBaseLine(load_customer, {'from':load_owner})
    
    time. sleep(5)

    contract.UpdateOracleData(load_customer, {'from':load_owner})

    return


def test_settle(set_deposit_amount, get_deployed_contract, load_customer, load_donor, load_owner):
    """
    This mocked version will always pay out to the customer because the oracle data always > baseline

    Check this is true
    """
    contract = get_deployed_contract
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')

    initial_balance = dai.balanceOf(load_customer)
    
    contract.settleAgreement(load_customer, {'from':load_owner})
    
    final_balance = dai.balanceOf(load_customer)
    
    assert(final_balance > initial_balance)

    return


def test_reset_fund_allocation(get_deployed_contract, load_owner,load_customer,load_donor):

    """
    
    this function transfers DAI between wallets to reset to the initial balances
    
    """

    contract = get_deployed_contract
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