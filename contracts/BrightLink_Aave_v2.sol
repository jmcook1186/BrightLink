// SPDX-License-Identifier: MIT
// this contract is deployed on Kovan at '0x15416033dBe9478e436d9DFfb625A5ab7758146D'

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolAddressesProviderV2.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolV2.sol";

contract BrightLink_Aave_v2 {

    uint256 depositedFunds;
    address private owner;
    uint16 referral = 0;
    address dai_address;
    address adai_address;
    address poolAddress;
    address poolAddressProvider;
    address customer;
    address donor;
    uint16 threshold;
    uint16 value;
    IERC20 dai;
    IERC20 adai;
    ILendingPoolV2 lendingPool;
    ILendingPoolAddressesProviderV2 provider;


    constructor(address _dai_address, address _adai_address, address _poolAddressProvider, address _customer, address _donor, uint16 _threshold) public{
        
        owner = msg.sender;
        customer = _customer;
        donor = _donor;
        depositedFunds = 0;
        dai_address = _dai_address;
        adai_address = _adai_address;
        poolAddressProvider = _poolAddressProvider;
        threshold = _threshold;
        dai = IERC20(dai_address);
        adai = IERC20(adai_address);
        provider = ILendingPoolAddressesProviderV2(poolAddressProvider); 
        poolAddress = provider.getLendingPool();
        lendingPool = ILendingPoolV2(poolAddress);

    }

    function lockDepositBalance() public onlyOwner{

        depositedFunds = dai.balanceOf(address(this));
    }

    function checkDepositAmount() public view returns(uint256 deposit){
        deposit = depositedFunds;
    }

    function checkBalance() public view returns (uint256 dai_balance, uint256 adai_balance) {
        // dai is held here, but aDai is sent to the owner's wallet so it can be used to yield farm
        dai_balance = dai.balanceOf(address(this));
        adai_balance = adai.balanceOf(address(this));

    }

    function depositFundsToAave() public onlyOwner{
	
        // Deposit dai and hold aDAI in contract.
        // pool requires approval to move DAI
        dai.approve(poolAddress,100000e18);
        dai.approve(address(this),100000e18);
        lendingPool.deposit(dai_address, dai.balanceOf(address(this)), address(this), referral);
        
    }


    function WithdrawFundsFromAave() public onlyOwner {
    	
    	// swap aDAI in contract for DAI
        // pool requires approval to move aDAI
        adai.approve(poolAddress,100000e18);
        adai.approve(address(this), 100000e18);
        lendingPool.withdraw(dai_address, adai.balanceOf(address(this)), address(this));

    }

    function setDummyTrigger(uint16 _value) public {

        value = _value;
    }


    function retrieveDAI() public onlyOwner{
        
        // send DAI from contract back to owner
        dai.approve(address(this), depositedFunds);
        dai.approve(customer, depositedFunds);
        dai.approve(donor, depositedFunds);

        if (value > threshold){
            
            require(dai.transfer(customer, depositedFunds));
            
            if (dai.balanceOf(address(this))>0){
                require(dai.transfer(owner,dai.balanceOf(address(this))));
            }
        }

        else{

            require(dai.transfer(donor, depositedFunds));
            
            if (dai.balanceOf(address(this))>0){

                require(dai.transfer(owner, dai.balanceOf(address(this))));
            }
        }

    }

    function escapeHatch() public onlyOwner{

        if (dai.balanceOf(address(this))>0){
            require(dai.transfer(owner,dai.balanceOf(address(this))));
        }
    
        if (adai.balanceOf(address(this))>0){
        require(adai.transfer(owner,adai.balanceOf(address(this))));
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
