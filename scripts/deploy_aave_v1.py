
#!/usr/bin/python3
from brownie import BrightLink_aave_v1, accounts, network


def main():

    account1 = load_account('main') # load account

    deploy_contract(account1)

    return


def load_account(accountName):

    account = accounts.load(accountName)

    return account


def deploy_contract(account1):

    print("Deploying contract to {} network".format(network.show_active()))
    BrightLink_aave_v1.deploy({'from':account1})

    return
