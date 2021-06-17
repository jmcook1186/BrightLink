
#!/usr/bin/python3
from brownie import BrightLink_Aave_v2, accounts, network, config


def main():

    owner = load_account('main') # load account
    customer = load_account('account2')
    donor = load_account('account3')
    dai_address = config["networks"][network.show_active()]["dai_address"]
    adai_address = config["networks"][network.show_active()]["adai_address"]
    poolAddressProvider = config["networks"][network.show_active()]["poolAddressProvider"]
    threshold = 5

    deploy_contract(owner,dai_address,adai_address,poolAddressProvider,customer,donor,threshold)

    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(owner,dai_address,adai_address,poolAddressProvider,customer,donor,threshold):

    print("Deploying contract to {} network".format(network.show_active()))
    BrightLink_Aave_v2.deploy(dai_address,adai_address,poolAddressProvider,customer,donor,threshold,{'from':owner})

    return
