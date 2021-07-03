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



def test_initial_balances(load_customer, getDeployedContract):
    """
    
    ensure contract and customer wallets are empty of DAI at start of testing

    """
    
    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    assert dai.balanceOf(contract) ==0
    assert adai.balanceOf(contract)==0
    assert dai.balanceOf(load_customer)==0

    return


def test_initial_deposit(set_deposit_amount, getDeployedContract, load_donor, load_owner):

    """
    ensure initial transfer of DAI from donor to contract executes correctly
    """

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


@pytest.mark.parametrize("wallet",
    [
     pytest.param('donor', marks=pytest.mark.xfail(reason="donor wallet does not have access to this function")),
     pytest.param('customer', marks=pytest.mark.xfail(reason="customer wallet does not have access to this function")),
     'owner'])

def test_move_funds_to_aave(set_deposit_amount, getDeployedContract, wallet, load_donor, load_customer, load_owner):
    
    """
    test transfer of funds from contract to aave lending pool
    parametrized test: iterates through 3 wallets. Only "owner" should have permisson, so 2/3 expected to fail.
    
    """
    if wallet == 'donor':
        wallet = load_donor
    elif wallet == 'customer':
        wallet = load_customer
    elif wallet == 'owner':
        wallet = load_owner
    else:
        raise("INVALID WALLET")

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    initialDaiBalance = dai.balanceOf(contract)
    initialAdaiBalance = adai.balanceOf(contract)

    assert initialDaiBalance == set_deposit_amount
    assert initialAdaiBalance == 0
    
    contract.depositFundsToAave({'from':wallet})

    time.sleep(10)

    finalDaiBalance = dai.balanceOf(contract)
    finalAdaiBalance = adai.balanceOf(contract)

    assert finalDaiBalance == 0
    assert finalAdaiBalance >= set_deposit_amount
    
    return


def test_aave_interest(getDeployedContract):
    
    """
    ensure funds in aave pool are accruing interest in
    the form of aDAI tokens in the contract
    """

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


@pytest.mark.parametrize("wallet",
    [
     pytest.param('donor', marks=pytest.mark.xfail(reason="donor wallet does not have access to this function")),
     pytest.param('customer', marks=pytest.mark.xfail(reason="customer wallet does not have access to this function")),
     'owner'
    ])
def test_withdrawal_from_aave(set_deposit_amount, getDeployedContract, wallet, load_donor, load_customer, load_owner):
    
    """
    test that funds can be withdrawn from aave lending pool back into contract
    parametrized test: iterates through 3 wallets. Only "owner" should have permisson, so 2/3 expected to fail.
    """

    if wallet == 'donor':
        wallet = load_donor
    elif wallet == 'customer':
        wallet = load_customer
    elif wallet == 'owner':
        wallet = load_owner
    else:
        raise("INVALID WALLET")

    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract

    contract.WithdrawFundsFromAave({'from': wallet})

    assert dai.balanceOf(contract) >= set_deposit_amount
    assert adai.balanceOf(contract) == 0

    return


def test_send_link(getDeployedContract, load_owner):
    
    """
    ensure contract receives LINK token to use as oracle gas
    """

    nLINK = 5e18
    link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')
    initial_LINK_balance = link.balanceOf(getDeployedContract)
    link.transfer(getDeployedContract,nLINK,{'from':load_owner})
    assert link.balanceOf(getDeployedContract) == initial_LINK_balance + nLINK

    return


@pytest.mark.parametrize("wallet",[
     pytest.param('donor', marks=pytest.mark.xfail(reason="donor wallet does not have access to this function")),
     pytest.param('customer', marks=pytest.mark.xfail(reason="customer wallet does not have access to this function")),
     'owner'
    ])
def test_set_weights(getDeployedContract, wallet, load_donor, load_customer, load_owner):
    
    """
    ensure that data can be requested from oracle
    test parametrized: only owner can access, expect 2/3 to fail

    """

    if wallet == 'donor':
            wallet = load_donor
    elif wallet == 'customer':
        wallet = load_customer
    elif wallet == 'owner':
        wallet = load_owner
    else:
        raise("INVALID WALLET")

    contract = getDeployedContract

    w1 = 100
    w2 = 100
    w3 = 100

    for i in [w1, w2, w3]:
        assert i <= 100

    contract.setWeights(w1, w2, w3,{'from':wallet})

    return



@pytest.mark.parametrize("wallet",[
     pytest.param('donor', marks=pytest.mark.xfail(reason="donor wallet does not have access to this function")),
     pytest.param('customer', marks=pytest.mark.xfail(reason="customer wallet does not have access to this function")),
     'owner'
    ])
def test_oracle_request(getDeployedContract, wallet, load_donor, load_customer, load_owner):
    
    """
    ensure that data can be requested from oracle
    test parametrized: only owner can access, expect 2/3 to fail

    """

    if wallet == 'donor':
        wallet = load_donor
    elif wallet == 'customer':
        wallet = load_customer
    elif wallet == 'owner':
        wallet = load_owner
    else:
        raise("INVALID WALLET")

    contract = getDeployedContract

    contract.requestDataFromAPI({'from':wallet})

    time.sleep(2)
    
    value = contract.viewValueFromOracle()
    
    # value from oracle should not be zero
    # it should be weighted mean of values
    # at each API endpoint
    assert value != 0

    return


def test_oracle_validation(getDeployedContract,load_owner):
    # no assert function required as the validation will simply
    # fail if there are less than 2 oracles returning good data
    contract = getDeployedContract
    contract.validateOracleData({'from':load_owner})

    return

@pytest.mark.parametrize("wallet",
    [
     pytest.param('donor', marks=pytest.mark.xfail(reason="donor wallet does not have access to this function")),
     pytest.param('customer', marks=pytest.mark.xfail(reason="customer wallet does not have access to this function")),
     'owner'
    ])
def test_withdrawal_from_contract(set_deposit_amount, getDeployedContract, wallet, load_owner, load_customer, load_donor, set_threshold):
    
    """
    ensure withdrawal of DAI from contract to recipient executs correctly.
    If oracle data > threshold, send to customer
    if oracle data < threshold, send to donor
    parametrized test: only "owner" has permission, so 2/3 expected to fail
    """    
    
    if wallet == 'donor':
        wallet = load_donor
    elif wallet == 'customer':
        wallet = load_customer
    elif wallet == 'owner':
        wallet = load_owner
    else:
        raise("INVALID WALLET")


    dai = interface.IERC20('0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD')
    adai = interface.IERC20('0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8')
    contract = getDeployedContract
    trigger = contract.viewValueFromOracle()

    assert adai.balanceOf(contract) == 0
    assert dai.balanceOf(contract) > set_deposit_amount

    initialOwnerBalance = dai.balanceOf(load_owner)
    initialCustomerBalance = dai.balanceOf(load_customer)
    initialDonorBalance = dai.balanceOf(load_donor)

    contract.retrieveDAI({'from':wallet})
    
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

    """
    
    this function transfers DAI between wallets to reset to the initial balances
    
    """

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