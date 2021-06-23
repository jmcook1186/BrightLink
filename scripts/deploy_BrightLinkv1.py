
#!/usr/bin/python3
from brownie import BrightLink_v01, accounts, network, config


def main():

    owner = load_account('main') # load account
    customer = load_account('account2')
    donor = load_account('account3')
    dai_address = config["networks"][network.show_active()]["dai_address"]
    adai_address = config["networks"][network.show_active()]["adai_address"]
    poolAddressProvider = config["networks"][network.show_active()]["poolAddressProvider"]
    link_address = config["networks"][network.show_active()]["link_address"]
    oracle_address = config["networks"][network.show_active()]["oracle"]
    oracle_fee = config["networks"][network.show_active()]["fee"]
    oracle_jobID = config["networks"][network.show_active()]["jobID"]
    threshold = 1500

    deploy_contract(owner,dai_address,adai_address,link_address,poolAddressProvider,\
        oracle_address, customer, donor, oracle_jobID, oracle_fee, threshold)


    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(owner,dai_address,adai_address,link_address,\
     poolAddressProvider,oracle_address,customer,donor,oracle_jobID, oracle_fee, threshold):

    assert network.show_active() == 'kovan'
    
    print("Deploying contract to {} network".format(network.show_active()))
    BrightLink_v01.deploy(dai_address, adai_address, link_address, poolAddressProvider,\
        oracle_address, customer, donor, oracle_jobID, oracle_fee, threshold, {'from':owner})

    return
