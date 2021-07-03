// SPDX-License-Identifier: MIT
// this contract is deployed on Kovan at '0x977B818C4df8559f76241Ce45ad856520d3B363c'

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolAddressesProviderV2.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolV2.sol";

contract BrightLink_v01 is ChainlinkClient {

    uint256 public depositedFunds;
    address private owner;
    uint16 private referral = 0;
    address public dai_address;
    address public adai_address;
    address public poolAddress;
    address public poolAddressProvider;
    address private customer;
    address private donor;
    uint16 private threshold;
    uint256 public value;
    address private oracle; // oracle address
    bytes32 private jobID; // oracle jobID
    uint256 private fee; // oracle fee
    string[3] public APIaddresses; 
    uint256[3] public oracleData;
    IERC20 public dai;
    IERC20 public adai;
    ILendingPoolV2 public lendingPool;
    ILendingPoolAddressesProviderV2 public provider;
    uint16 index = 0;
    uint256 aggregateData;

    constructor(address _dai_address, address _adai_address, address _link, address _poolAddressProvider,
    address _oracle, address _customer, address _donor, string memory _jobID, uint256 _fee, uint16 _threshold) public{
    
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
        oracle = _oracle;
        jobID = stringToBytes32(_jobID);
        fee = _fee;
        APIaddresses[0] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/example.json";
        APIaddresses[1] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/example2.json";
        APIaddresses[2] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/example3.json";
        oracleData[0] = 0;
        oracleData[1] = 0;
        oracleData[2] = 0;

        
        // set link token address depending on network
        if (_link == address(0)) {
            setPublicChainlinkToken();
        } else {
            setChainlinkToken(_link);
        }

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


    function requestDataFromAPI() public onlyOwner{

        oracleRequest(APIaddresses[0]);
        oracleRequest(APIaddresses[1]);
        oracleRequest(APIaddresses[2]);
    
    }


    function oracleRequest(string memory url) internal returns (bytes32 requestId) 
    {
        Chainlink.Request memory request = buildChainlinkRequest(jobID, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", url);
        request.add("path", "data.0.number");
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    function fulfill(bytes32 _requestId, uint256 _value) public recordChainlinkFulfillment(_requestId)
    
    {

        oracleData[index] = _value; 
        // This ensures the array never goes past 3, we just keep rotating responses
        index = (index + 1) % 3;
        aggregateData = (oracleData[0]+oracleData[1]+oracleData[2])/3;

    }

    function viewValueFromOracle() public view returns(uint256 viewValue){
        
        viewValue = aggregateData;
    }


    function retrieveDAI() public onlyOwner{
        
        // send DAI from contract back to owner
        dai.approve(address(this), depositedFunds);
        dai.approve(customer, depositedFunds);
        dai.approve(donor, depositedFunds);

        if (aggregateData > threshold){
            
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

    function retrieveLINK() public onlyOwner{
        
        // instantiate LINK token
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());

        // transfer remaining contract LINK balance to sender
        require(link.transfer(owner, link.balanceOf(address(this))), "Unable to transfer");
    }


    function escapeHatch() public onlyOwner{

        if (dai.balanceOf(address(this))>0){
            require(dai.transfer(owner,dai.balanceOf(address(this))));
        }
    
        if (adai.balanceOf(address(this))>0){
        require(adai.transfer(owner,adai.balanceOf(address(this))));
        }

        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        if (link.balanceOf(address(this))>0){
        require(link.transfer(msg.sender, link.balanceOf(address(this))), "Unable to transfer");
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
