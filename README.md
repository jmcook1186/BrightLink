# BRIGHTLINK

*NB: This repository is in active development and does not yet have full functionality.

July 2021: payouts now triggered by aggregate (weighted mean) of 3 chainlink oracle requests
June 2021: Only v1 of the financial model is actually implemented in the repository.

Ongoing blog posts about this project development can be found at [www.tothepoles.co.uk/](https://tothepoles.co.uk/category/eolink/)*


## Outline
This system incentivizes hypothetical communities to "brighten" their local environment. There are two use-cases in this repository:

### Purpose

1) Environmental organizations are incentivized to "brighten" snow, ice and sea ice surfaces to slow their rate of melting. This is currently achieved occasionally using light-scattering sand or strategically-placed white sheets and has the effect of slowing sea ice retreat and prolonging the life of snowpacks for ski resorts etc. The degree to which brightening occurs will be determined as a function of the deviation in the surface albedo derived from Sentinel-2 imagery relative to a baseline.

2) A community is incentivized to "green" their local environment by conserving and adding vegetated land (replanting verges, rooftop gardens, etc..). The payout is scaled by the % change in "green" area within the area of interest. The surface greening calculation is achieved using a supervised classification algorithm applied to multispectral Sentinel-2 satellite data.

3) Other applications could include incentivizing beach clean-ups by remotely quantifying beach litter using drone data, etc


### Financial Model

The initial capital comes from a donor individual or organization who wishes to incentivizes a second organization or individual to brighten a specific area of interest. This initial donation is sent into escrow in the BrightLink Solidity contract in DAI.

The contract then places those in a DeFi strategy where they accrue interest. The interest is profit for the contract owner, generating income without decrementing the initial donated capital. When the consumer organization triggers a settlement, or some predetermined time has elapsed, the funds are pulled from the Aave pool, the interest that accrued is released to the contract owner as profit, and the initial capital remains in escrow in the contract, ready to be paid out at a rate that depends on the degree to which the consumer has achieved its goals.</p>

### Mechanism


The contract contains a function that triggers a Chainlink oracle to make a GET request to an API endpoint. That API endpoint is a json file that contains the results of a satellite remote sensing script run externally. When the remote sensing script finishes executing it updates the json file with the most recent remote sensing data. On request, the chainlink oracle ingests that data into the smart contract. This happens twice - first to establish an initial baseline which becomes the target value for the consumer organization to try to beat. Then, after some predetermined time has passed, the contract is called again and the updated remote sensing data is used to determine the amount of DAI that should be removed from the Aave pool and paid out. 

### Remote Sensing


Precise details of the remote sensing app are TBC, but I intend to build a Sentinel-2 supervised classification scheme and chlorophyll-index calculation to determine surface greening, and a narrow-broadband albedo calculation to determine surface brightening. The result will be some spatial statistic (e.g. area-mean albedo, total chlorophyll) compared to a baseline value.


## Prerequisites

Please install or have installed the following:

- [nodejs and npm](https://nodejs.org/en/download/)
- [python](https://www.python.org/downloads/)
- 
## Installation

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) 

```bash
pip install eth-brownie
```

2. [Install ganache-cli](https://www.npmjs.com/package/ganache-cli)

```bash
npm install -g ganache-cli
```

3. This project deploys to the Kovan testnet. This requires an Infura project ID and your wallet's private key to be provided in a .env file (not 
provided in this git repository).

You can get a `WEB3_INFURA_PROJECT_ID` by getting a free trial of [Infura](https://infura.io/). You can [follow this guide](https://ethereumico.io/knowledge-base/infura-api-key-guide/) to getting a project key. You can find your `PRIVATE_KEY` from your ethereum wallet like [metamask](https://metamask.io/). 

You can add your environment variables to the `.env` file:

```
export WEB3_INFURA_PROJECT_ID=<PROJECT_ID>
export PRIVATE_KEY=<PRIVATE_KEY>

```

4. Your wallet requires Kovan test ETH and test-LINK.
   
   DO NOT USE REAL ASSETS. DO NOT SEND ASSETS FROM A MAINNET WALLET TO A KOVAN ADDRESS. DO NOT USE YOUR MAINNET ACCOUNT IN A DEVELOPMENT ENVIRONMENT.
   
   See instructions [here](https://faucet.kovan.network/) and [here](https://docs.chain.link/docs/acquire-link/)


## Testing

Testing is achieved using pytest in brownie. I have not yet written any mocks, so all tests use the contracts deployed on the Kovan testnet. Fixtures (configuration common to all tests) are defined in conftest.py and unit tests are defined in test_flood_insurance.py. To run the tests from the terminal, navigate to the project folder, then:

```
>>> brownie test --network kovan

```


## Resources

To get started with Brownie:

* [Chainlink Documentation](https://docs.chain.link/docs)
* Check out the [Chainlink documentation](https://docs.chain.link/docs) to get started from any level of smart contract engineering. 
* Check out the other [Brownie mixes](https://github.com/brownie-mix/) that can be used as a starting point for your own contracts. They also provide example code to help you get started.
* ["Getting Started with Brownie"](https://medium.com/@iamdefinitelyahuman/getting-started-with-brownie-part-1-9b2181f4cb99) is a good tutorial to help you familiarize yourself with Brownie.
* For more in-depth information, read the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/).

Explainers for this specific repository:
* [www.tothepoles.co.uk](https://tothepoles.co.uk/2021/06/04/eolink-0-1-3-simplified-flood-insurance/)


## License

This project is licensed under the [MIT license](LICENSE).# BrightLink
