// SPDX-License-Identifier: MIT
// this contract is deployed on Kovan at 0xb7A997C957bF86E82ea5804c301142eF07c36829

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolAddressesProviderV2.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolV2.sol";

contract BrightLink_Aave_v1 {

    uint256 depositedFunds;
    address private owner;
    uint16 referral = 0;
    address dai_address = 0xFf795577d9AC8bD7D90Ee22b6C1703490b6512FD;
    address adai_address = 0xdCf0aF9e59C002FA3AA091a46196b37530FD48a8;
    address poolAddress;
    IERC20 dai = IERC20(dai_address);
    IERC20 adai = IERC20(adai_address);
    ILendingPoolV2 lendingPool;
    ILendingPoolAddressesProviderV2 provider;


    constructor() public{
        
        owner = msg.sender;
        depositedFunds = 0;
        provider = ILendingPoolAddressesProviderV2(address(0x88757f2f99175387aB4C6a4b3067c77A695b0349)); 
        poolAddress = provider.getLendingPool();
        lendingPool = ILendingPoolV2(poolAddress);

    }

    function checkBalance() public view returns (uint256 dai_balance, uint256 adai_balance) {
        // dai is held here, but aDai is sent to the owner's wallet so it can be used to yield farm
        dai_balance = dai.balanceOf(address(this));
        adai_balance = adai.balanceOf(address(this));

    }

    function depositFundsToAave() public onlyOwner{
	
        depositedFunds += dai.balanceOf(address(this));

        // Deposit dai and hold aDAI in contract.
        // pool requires approval to move DAI
        dai.approve(poolAddress,100000e18);
        dai.approve(address(this),100000e18);
        lendingPool.deposit(dai_address, dai.balanceOf(address(this)), address(this), referral);
        
    }

    function viewDeposits() public view returns (uint256 deposits){
        
        deposits = depositedFunds;
    
    }

    function viewProfit() public view returns(uint256 profit){

        profit = adai.balanceOf(address(this)) - depositedFunds;

    }

    function WithdrawFundsFromAave() public onlyOwner {
    	
    	// swap aDAI in contract for DAI
        // pool requires approval to move aDAI
        adai.approve(poolAddress,100000e18);
        adai.approve(address(this), 100000e18);
        lendingPool.withdraw(dai_address, adai.balanceOf(address(this)), address(this));
    
    }

    function retrieveDAI() public onlyOwner{
        
        // send DAI from contract back to owner
        if (dai.balanceOf(address(this)) >0){
            require(dai.transfer(owner, dai.balanceOf(address(this))));
        }

        // send aDAI from contract back to owner
        if (adai.balanceOf(address(this)) > 0){
            require(adai.transfer(owner, adai.balanceOf(address(this))));
        }
    
    }


    // ACCESSORY FUNCTIONS
    
        modifier onlyOwner(){
        require(owner==msg.sender);
        _;
    }
    
    function stringToBytes32(string memory source) public pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            result := mload(add(source, 32))
        }
    }
}
