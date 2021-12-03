# BrightLink Design Decisions

## Restricting access

onlyOwner modfier restricts anyone but the contract owner from taking profits
moving funds in and out of aave can only be done by internal functions

## Inheritance and inter-contract execution
BrightLink contract inherits from chainlink and also uses the IERC20 contract from open zeppelin
BrightLink contract also uses a lendng pool provider contract for Aave lending pool

## Oracles
BrightLink contract makes calls to external API using a Chainlink oracle, synthesizes and updates contract state

## upgradeable contracts
Aave pool uses a lending pool provider contract

## State Machine
Mapping keeps track of status of customer/donor agreements, current data etc
Settling agreement nullifies data in mapping

## Circuit Breaker
"EscapeHatch" function withdraws all unspent funds back to the contract owner  