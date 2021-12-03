# blockchain-developer-bootcamp-final-project

# Urban-Greening app
## Satellite-verified greening of urban environments

This app will allow donors to escrow money in a smart contract as an incentive for a community to "green" a target area. Greening can include rooftop gardens, planting on verges and scrub-land, reforesting, etc. The donated funds are paid out if, and only if, the target area is demonstrably greener after a set time has elapsed. This is measured using satellite remote sensing. Multispectral sensors onboard NASA'a MODIS and LANDSAT and ESA's Sentinel-2 platforms have sufficient spectral resolution to detect chlorophyll using its reflectance signature. Chlorophyll is unique to photosynthetic plants and algae, and is therefore diagnostic of added vegetation in an urban environment. Using the chlorophyll index prtects against communities gaming the system by laying astroturf or painting surfaces green, and also enables expansion of the term "greening" to include improving the health of existing vegetation as well as adding more, since healthier plants produce more chlorophyll.

To achieve this, a financial model will be encoded in a Solidity smart contract and deployed to an Ethereum testnet (kovan). A donor will deposit funds into the contract along with a target change in chlorophyll index and an address for the payee. For example, a donor might say that 10,000 DAI is available if a community manages to green by 10% above its baseline. The basline chlorophyll index for a target area will be determined by making an external call through a Chainlink oracle to three bespoke Google Earth Engine apps hosted on Heroku. This will accept polygon coordinates for the target area, start and end times as arguments and will return the area-averaged chlorophyll index averaged over the given dates (eg. the mean for the 3 most recent summers) as a uint. This will act as the threshold for determining a payout later. After a set time, the contract will trigger the chainlink oracle a second time to gather updated measurements. If the difference between initial and final measurements exceeds the given threshold, the payee automatically receives the donated funds. If not, the funds are returned to the donor. In the mean time, the contract deposits the funds in an Aave lending pool where it accrues yield. That yield is kept as profit for the platform.

### Embedded DeFi

This platform makes a profit during the time between a new project being agreed and the payout. This is achieved using an internal function that takes the deposited funds and sends them to an Aave lending pool. When a payout is requested, the funds are withdrawn from the Aave pool back into the contract. The principal is then paid out according to the results of the urban greening, while the remainder is accumulated as profit in the contract which can be retrived at any time by the contract owner. <b>please note</b> this functionality will not be apparent from interacting with the system via the public frontend - but the video walkthrough demonstrates how it works and if you wish you can use brownie console to replicate using instructions below.

### Mechanism

The contract contains a function that triggers a Chainlink oracle to make a GET request to an API endpoint. That API endpoint is a json file that contains the results of a satellite remote sensing script run externally. When the remote sensing script finishes executing it updates the json file with the most recent remote sensing data. On request, the chainlink oracle ingests that data into the smart contract. This happens twice - first to establish an initial baseline which becomes the target value for the consumer organization to try to beat. Then, after some predetermined time has passed, the contract is called again and the updated remote sensing data is used to determine the amount of DAI that should be removed from the Aave pool and paid out. 

### Remote Sensing

For the community greening project the remote sensing scripts use Google Earth Engine to calculate the normalised-difference vegetation index for the given area on the given dates. This is done using three separate data sources from three different satellites (Landsat, MODIS, Sentinel-2). For each dataset, the ndvi is averaged (arithmetic mean) over time and space to give a single value for the ndvi of the region for the given time period. The three values (one from each satellite) are each pulled onchain by a chainlink oracle using the weighted mean. By default, the three satellites are equally weighted, but the contract owner can update this as necessary (.e.g if the lower resolution of MODIS gives less confidence, if one dataset has more cloudy images, etc). <b>please note</b> in this submission, to avoid having to either share my google earth engine credentials or rely on the assessor signing up to google-earth-engine I have simply mocked this with a static endpoint. I also decided, for simplicity, not to add site coordinates as an input field, instead in this proof-of-concept version has fixed site coordinates.

## Public URL

The public front-end for this project is at "https://yeti87803643.github.io/blockchain-developer-bootcamp-final-project/". Here, a user can connect using MetaMask and interact with the contract. Please note that the front end only allows a user to register a new agreement, wait some period of time, then request a settlement. This is super simple and the correct functionality can be observed by watching the balances of the relevant accounts. The walkthrough video shows the more interesting functionality (profit generation via aave lending, updating staellite remote sensing values).

<img src="/Assets/app_screenshot.png" width=1500>

## Ethereum Address

The NFT for the project completion can be sent to my ENS name: jmcook.eth

## VIDEO WALKTHROUGH

A video walkthrough of this dapp is available [HERE](https://youtu.be/n783zeTC3bk)

## MOCKING

Ths app currently requires Google Earth Engine login credentials to update the vegetation index for a given location. Therefore, for this submission I decided to mock the API endpoints queried by the Chainlink oracles. They stay constant and therefore a payout should be returned to the donor rather than awarded to the customer in this version of the system (there is another version, closer to production, for which this is not the case, at www.github.com/jmcook1186/Brightlink) but I reasoned that this version wouold be harder to evaluate for the bootcamp as it currently has awkward dependencies that I was not able to resolve before the submission deadline. I also decided not to include site coordinates as in input field as the app was becoming quite complicatedand the UX was not great. I decided for this submission, fixed site coordinates were best, with variable coordinates coming in a later update.

## Directory Structure

Please see file dir_tree.md for an annotated schematic of the project directory structure.


## Instructions
### Using the App
### This version is deployed on Kovan only. This is because it relies upon having wallets funded with testnet ETH, DAI and LINK and I wasn't able to pre-fund wallets fo multiple testnets in time for the project submission.

#### 0) IF NECESSARY, CREATE PYTHON ENVIRONMENT FROM YAML
The environment.yaml file contained in this repository's root directory contains all the dependencies required to run this app, includign Brownie and Ganache.

`conda create -f environment.yaml `

activate the environment

`source activate BlockChain`

#### 1) ADD ACCOUNTS. 

I have prefunded three dummy accounts on Kovan with ETH, DAI and LINK to enable this app to be used by the assessors. Running from "main" account allows onlyOwner privelages in contract, others are arbitrary but contain funds for convenience and should be named "account2" and "account3" so the automated tests can load them by name). These dummy accounts have only ever been used on testnets and never touched mainnet or any L2. They can be imported to MetaMask. 

You are also welcome to redeploy a fresh instance of the contract with your own account as the contract owner - just update .env and run:

```
brownie run ./scripts/deploy_BrightLinkv1.py

```

#### 2) POPULATE .ENV

I have included a file .env_example in this repository. Rename it .env and fill in the spaces with your Infura project ID, private key and Git personal authentication token. The private key to use is the one provided above for account "main". This will ensure the wallet is funded with sufficient ETH, LINK and DAI and give onlyOwner privelages. The Git personal auth token is optional and only required if the remote sensing scripts are being run (probably not for assessment as I have mocked everything).

3) Decide which account represents the "donor" who is putting in funds. Approve dai spending from this account:
```bash
brownie console --network kovan

```
```python
donor = accounts.load(account3)
dai = interface.ERC20('0xff795577d9ac8bd7d90ee22b6c1703490b6512fd')
dai.approve(contract.address, 2000e18,{'from':donor})
```

#### 3) Pre-fund the contract with some LINK
(in brownie console)
```
link = interface.LinkTokenInterface('0xa36085F69e2889c224210F603D836748e7dC0088')
link.transfer(contract,0.6,{'from':owner})

```
#### 4) Open app in web browser, add accounts to MetaMask
   (alternatively run from localhost by opening a new console, navigating to ./client/src and `npm run start`)
#### 5) Connect "main" account to app
#### 6) Provide address for customer (account 2) and donor (account3)
#### 7) Click CONFIRM (the DAI balance for the don or will decrease by the setllement amount)
   (make sure the connected wallet is open in metamask when the confirm button is clicked)
#### 7) When some time has passed, click SETTLE the balances will redress
#### 8)  click "documentation" in lower right corner for more information


### Running Automated tests

1) ACTIVATE BROWNIE ENVIRONMENT
   `source activate BlockChain`

2) To run unit tests (i.e. individual functions tested separately):
`brownie test ./tests/unitary --network kovan`

1) To run integration test (i.e. single test covering a complete end-to-end use of the contract):
`brownie test ./tests/integrative --network kovan` 

4) If the initial test fails, it is likely because there is some residual DAI sitting in the contract from previous interactions. If this is the case it can easily be fixed by calling the "escapeHatch()" function in the contract as follows:

```bash
brownie console --network kovan
```
```
contract = Contract(<contract_address>)
owner = accounts.load("main")
contract.escapeHatch({'from':owner})
```

This will reset the contract balance and the tests should now pass. This should not be necessary as it should be handled inside the testing script, but just in case.