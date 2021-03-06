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
    return 1000

@pytest.fixture(scope="module")
def get_deployed_contract():
    return Contract('0xB5600D46f8e7191B3791eCCEC7697a537976d4d5')

@pytest.fixture(scope='module')
def set_deposit_amount():
    return 2000e18

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
