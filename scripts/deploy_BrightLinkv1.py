
#!/usr/bin/python3
from brownie import BrightLink, accounts, network, config


def main():

    owner = load_account('main') # load account

    dai_address = config["networks"][network.show_active()]["dai_address"]
    adai_address = config["networks"][network.show_active()]["adai_address"]
    poolAddressProvider = config["networks"][network.show_active()]["poolAddressProvider"]
    link_address = config["networks"][network.show_active()]["link_address"]
    oracle_address = config["networks"][network.show_active()]["oracle"]
    oracle_fee = config["networks"][network.show_active()]["fee"]
    oracle_jobID = config["networks"][network.show_active()]["jobID"]

    deploy_contract(owner,dai_address,adai_address,link_address,poolAddressProvider,\
        oracle_address, oracle_jobID, oracle_fee)


    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(owner,dai_address,adai_address,link_address,\
     poolAddressProvider,oracle_address,oracle_jobID, oracle_fee):

    assert network.show_active() == 'kovan'
    
    print("Deploying contract to {} network".format(network.show_active()))
    BrightLink.deploy(dai_address, adai_address, link_address, poolAddressProvider,\
        oracle_address, oracle_jobID, oracle_fee, {'from':owner})

    return
