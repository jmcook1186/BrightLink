This file contains the directory structure for the BrightLink project with annotations

```
.
├── app                                     //(contains files relating to remote sensing app)
│   ├── ImageAnalysis.py                    
│   ├── main.py
│   ├── Procfile
│   ├── requirements.txt
│   └── run.py
|
├── Assets
│   ├── app_screenshot.png        // screenshot for README
│   
|
├── avoiding_common_attacks.md     // info about contract security
├── brownie-config.yaml            //  brownie config info incl. contract addresses
├── client                          // front-end top level dir
│   ├── build                       
│   │   ├── asset-manifest.json
│   │   ├── favicon.ico
│   │   ├── index.html
│   │   ├── logo192.png
│   │   ├── logo512.png
│   │   ├── manifest.json
│   │   ├── robots.txt
│   │   └── static
|   |
│   ├── package.json           // dependencies
│   ├── package-lock.json
│   ├── public
|   |
|   |
│   ├── README.md
│   ├── src
│   │   ├── App.css
│   │   ├── App.js
│   │   ├── App.test.js
│   │   ├── artifacts
│   │   │   ├── contracts
│   │   │   │   ├── BrightLink.json
│   │   │   │   ├── dependencies
│   │   │   │   │   ├── OpenZeppelin
│   │   │   │   │   │   └── openzeppelin-contracts@3.4.0
│   │   │   │   │   │       └── IERC20.json
│   │   │   │   │   └── smartcontractkit
│   │   │   │   │       └── chainlink-brownie-contracts@1.0.2
│   │   │   │   │           ├── BasicToken.json
│   │   │   │   │           ├── BufferChainlink.json
│   │   │   │   │           ├── CBORChainlink.json
│   │   │   │   │           ├── ChainlinkClient.json
│   │   │   │   │           ├── Chainlink.json
│   │   │   │   │           ├── ChainlinkRequestInterface.json
│   │   │   │   │           ├── ENSInterface.json
│   │   │   │   │           ├── ENSResolver.json
│   │   │   │   │           ├── ERC20Basic.json
│   │   │   │   │           ├── ERC20.json
│   │   │   │   │           ├── ERC677.json
│   │   │   │   │           ├── ERC677Receiver.json
│   │   │   │   │           ├── ERC677Token.json
│   │   │   │   │           ├── LinkTokenInterface.json
│   │   │   │   │           ├── PointerInterface.json
│   │   │   │   │           ├── SafeMathChainlink.json
│   │   │   │   │           └── StandardToken.json
│   │   │   │   └── LinkToken.json
│   │   │   ├── deployments
│   │   │   │   ├── 1
│   │   │   │   ├── 42
│   │   │   │   │   ├── 0x051c2B9fcCcf0ca4BfB73c7FF5e4759D851075EE.json
│   │   │   │   │   └── 0xC2089D4B373F5644fB37C6bd40D91F71092e8Ba3.json
│   │   │   │   ├── dev
│   │   │   │   └── map.json
│   │   │   ├── interfaces
│   │   │   │   ├── ILendingPoolAddressesProviderV2.json
│   │   │   │   ├── ILendingPoolV2.json
│   │   │   │   └── LinkTokenInterface.json
│   │   │   └── tests.json
│   │   ├── getEthereum.js
│   │   ├── getWeb3.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── logo.svg
│   │   ├── reportWebVitals.js
│   │   ├── setupTests.js
│   │   ├── SolarPunkPaintingFull.jpg
│   │   ├── SolarPunkPainting.jpg
│   │   ├── SolarPunkPainting.png
│   │   ├── TreeBorder2.jpg
│   │   └── TreeBorder.jpg
│   └── yarn.lock
├── contracts                  // Ethereum smart contracts
│   ├── BrightLink.sol
│   └── test
│       └── LinkToken.sol
├── contract.sol
├── deployed_address.txt
├── design_pattern_decisions.md
├── dir_tree.txt
├── environment.yaml                //python environment for brownie
├── interfaces
│   ├── ILendingPoolAddressesProviderV2.sol
│   ├── ILendingPoolV2.sol
│   └── LinkTokenInterface.sol
├── libraries
│   └── DataTypes.sol
├── LICENSE
├── README.md
├── reports
│   └── coverage.json
├── requirements.txt
├── scripts
│   ├── deploy_BrightLinkv1.py
│   └── remote_sensing
│       ├── app.py
│       ├── ImageAnalysisDriver.py
│       ├── ImageAnalysis.py

└── tests
    ├── integrative
    │   ├── conftest.py
    │   └── test_system.py
    └── unitary
        ├── conftest.py
        └── test_system.py

```