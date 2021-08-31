import pytest

from brownie import (
    BrightLink,
    Contract,
    accounts,
    network,
)

@pytest.fixture
def checkNetwork():
    assert network.show_active() == 'kovan'
    return

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

@pytest.fixture(scope="module")
def getDeployedContract(load_owner):
    contract = load_owner.deploy(BrightLink,'0xff795577d9ac8bd7d90ee22b6c1703490b6512fd',\
        '0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8',\
            '0xa36085F69e2889c224210F603D836748e7dC0088',\
                '0x88757f2f99175387aB4C6a4b3067c77A695b0349',\
                    '0xc57B33452b4F7BB189bB5AfaE9cc4aBa1f7a4FD8',\
                        'd5270d1c311941d0b08bead21fea7747',\
                            100000000000000000)
    return contract

@pytest.fixture(scope='module')
def set_deposit_amount():
    return 500e18

