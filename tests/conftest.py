import pytest

from brownie import (
    Contract,
    accounts,
    network,
)

@pytest.fixture
def checkNetwork():
    assert network.show_active() == 'kovan'
    return

@pytest.fixture
def set_threshold():
    return 5

@pytest.fixture
def set_trigger_value():
    return 7

@pytest.fixture(scope="module")
def getDeployedContract():
    return Contract('0x450Aab7b234314E07B0c304Cb26cCAC231B0ceF2')

@pytest.fixture(scope='module')
def set_deposit_amount():
    return 5000e18

@pytest.fixture(scope='module')
def load_owner():
    owner = accounts.load('main')
    return owner

@pytest.fixture(scope='module')
def load_customer():
    customer = accounts.load('account2')
    return customer

@pytest.fixture(scope='module')
def load_donor():
    donor = accounts.load('account3')
    return donor
