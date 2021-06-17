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


@pytest.fixture(scope="module")
def getDeployedContract():
    return Contract('0xb7A997C957bF86E82ea5804c301142eF07c36829')

@pytest.fixture(scope='module')
def set_deposit_amount():
    return 2000e18

@pytest.fixture(scope='module')
def load_account():
    account1 = accounts.load('main')
    return account1

