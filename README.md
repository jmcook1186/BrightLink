# BRIGHTLINK

Brightlink is a PoC project that shows how communities can be incentivized to "brighten" their local environments. There are two examples implemented in this repository:

2) A community is incentivized to "green" their local environment by conserving and adding vegetated land (replanting verges, rooftop gardens, etc..) and engaging in urban agriculture. This is measured by quantifying the NDVI chlorophyll index across the area of interest using multispectral data from three satellites (MODIS, LANDSAT, Sentinel2).

3) Environmental organizations are incentivized to "brighten" snow, ice and sea ice surfaces to slow their rate of melting. This is currently achieved occasionally using light-scattering sand or strategically-placed white sheets and has the effect of slowing sea ice retreat and prolonging the life of snowpacks for ski resorts etc. The degree to which brightening occurs will be determined as a function of the deviation in the surface albedo derived from Sentinel-2 imagery relative to a baseline.

The general model is that a donor defines a reward, target and time period, for example they may propose that a 10,000 DAI reward is available for a 15% increase in the detectable vegetation in a town over summer (June-August). This becomes encoded logic in the BrightLink smart contract. This includes the previous year's data being generated as a baseline to compare against by running the geospatial processing scripts. After the set time period, the scripts are run again to get updated estimates. If the updated data is sufficiently improved against the baseline, then the donated DAI is paid out to the community wallet. If not, the DAI is returned to the donor. In between times, the DAI is held in an Aave lending pool, generating profit for the BrightLink platform.

Ongoing blog posts about this project development can be found at [www.tothepoles.co.uk/](https://tothepoles.co.uk/category/eolink/)*

### Mechanism

The contract contains a function that triggers a Chainlink oracle to make a GET request to an API endpoint. That API endpoint is a json file that contains the results of a satellite remote sensing script run externally. When the remote sensing script finishes executing it updates the json file with the most recent remote sensing data. On request, the chainlink oracle ingests that data into the smart contract. This happens twice - first to establish an initial baseline which becomes the target value for the consumer organization to try to beat. Then, after some predetermined time has passed, the contract is called again and the updated remote sensing data is used to determine the amount of DAI that should be removed from the Aave pool and paid out. 

### Remote Sensing

For the community greening project the remote sensing scripts use Google Earth Engine to calculate the normalised-difference vegetation index for the given area on the given dates. This is done using three separate data sources from three different satellites (Landsat, MODIS, Sentinel-2). For each dataset, the ndvi is averaged (arithmetic mean) over time and space to give a single value for the ndvi of the region for the given time period. The three values (one from each satellite) are each pulled onchain by a chainlink oracle using the weighted mean. By default, the three satellites are equally weighted, but the contract owner can update this as necessary (.e.g if the lower resolution of MODIS gives less confidence, if one dataset has mre cloudy images, etc).



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


5. Google Earth Engine
   you need a GEE account and the GEE packages installed in the development environment

6. GIT
   A Github account with the auth token in .env




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

This project is licensed under the [MIT license](LICENSE).
