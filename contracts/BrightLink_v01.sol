// SPDX-License-Identifier: MIT
// this contract is deployed on Kovan at 

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/ChainlinkClient.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolAddressesProviderV2.sol";
import "/home/joe/Code/BrightLink/interfaces/ILendingPoolV2.sol";

contract BrightLink_v02 is ChainlinkClient {

    // var definitions
    uint256 public depositedFunds;
    address private owner;
    uint16 private referral = 0;
    address public dai_address;
    address public adai_address;
    address public poolAddress;
    address public poolAddressProvider;
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
    uint16 index;
    uint256 aggregateData;
    uint16 w1;
    uint16 w2;
    uint16 w3;
    uint16 minResponses = 2;
    uint16 badOracles = 0;
    int Id = 0;
    mapping(address => int) private customerToAgreementID;
    mapping(address => int) private donorToAgreementID;
    mapping(int => address) private agreementIdToDonor;
    mapping(int => uint256) private agreementIdToBaseline;
    mapping(int => uint256) private agreementIdToValue;
    mapping (int => uint256) public agreementIdToRetrievedData;

    constructor(address _dai_address, address _adai_address, address _link, address _poolAddressProvider,
    address _oracle, string memory _jobID, uint256 _fee) public{
        
        // var instantiations
        owner = msg.sender;
        depositedFunds = 0;
        dai_address = _dai_address;
        adai_address = _adai_address;
        poolAddressProvider = _poolAddressProvider;
        dai = IERC20(dai_address);
        adai = IERC20(adai_address);
        provider = ILendingPoolAddressesProviderV2(poolAddressProvider); 
        poolAddress = provider.getLendingPool();
        lendingPool = ILendingPoolV2(poolAddress);
        oracle = _oracle;
        jobID = stringToBytes32(_jobID);
        fee = _fee;
        APIaddresses[0] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/BrightLinkData/SentinelData.json";
        APIaddresses[1] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/BrightLinkData/LandsatData.json";
        APIaddresses[2] = "https://raw.githubusercontent.com/jmcook1186/jmcook1186.github.io/main/Data/BrightLinkData/ModisData.json";
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

    /**
    @dev
    requires donor to approve dai transfer before function is called:
    dai.approve(contract,200e18,{'from':donor})

     */
    function addNewCustomer(address _customer, address _donor, uint256 _baseline, uint256 _value) public onlyOwner {

        require(dai.transferFrom(_donor, address(this), _value));
        depositedFunds += _value;
        customerToAgreementID[_customer] = Id;
        donorToAgreementID[_donor] = Id;
        agreementIdToBaseline[Id] = _baseline;
        agreementIdToValue[Id] = _value;
        agreementIdToDonor[Id]  = _donor;
        depositFundsToAave();
        Id+=1; 
    }


    function depositFundsToAave() internal {
	
        // Deposit dai in lending pool and receive aDAI in contract.
        // pool requires approval to move DAI
        dai.approve(poolAddress,1000000e18);
        dai.approve(address(this),1000000e18);
        lendingPool.deposit(dai_address, dai.balanceOf(address(this)), address(this), referral);
        
    }

    function WithdrawFundsFromAave(uint _amount) public onlyOwner {
    	
    	// swap aDAI in contract for DAI
        // pool requires approval to move aDAI
        adai.approve(poolAddress, _amount);
        adai.approve(address(this), _amount);
        lendingPool.withdraw(dai_address, _amount, address(this));

    }

    function setWeights(uint16 _w1, uint16 _w2, uint16 _w3) public onlyOwner{
        // weights for averaging oracle data
        // eventually, weights could be set by voting ina DAO

        w1 = _w1;
        w2 = _w2;
        w3 = _w3;

    }


    function setBaseLine(address _customer, uint16 _w1, uint16 _w2, uint16 _w3) public onlyOwner {
        
        int id = customerToAgreementID[_customer];
        setWeights(_w1, _w2, _w3);
        requestDataFromAPI();
        validateOracleData();
        agreementIdToBaseline[id] = aggregateData;

    }


    function UpdateOracleData(address _customer) public onlyOwner {
        
        int id = customerToAgreementID[_customer];
        requestDataFromAPI();
        validateOracleData();
        agreementIdToRetrievedData[id] = aggregateData;

    }



    function settleAgreement(address _customer) public onlyOwner onlyForValidOracles{
        
        int agreementId = customerToAgreementID[_customer];
        uint256 amount = agreementIdToValue[agreementId];
        uint256 threshold = agreementIdToBaseline[agreementId];
        address donor = agreementIdToDonor[agreementId];
        address customer = _customer;
        uint256 retrieval = agreementIdToRetrievedData[agreementId];

        // send DAI from contract back to owner
        dai.approve(address(this), amount);
        dai.approve(customer, amount);

        if (retrieval > threshold){
            
            require(dai.transfer(customer, amount));
            
            if (dai.balanceOf(address(this))>0){
                require(dai.transfer(owner,amount));
            }
        }

        else{

            require(dai.transfer(donor, amount));
            
            if (dai.balanceOf(address(this))>0){

                require(dai.transfer(owner, amount));
            }

        // set transaction value to 0 to prevent re-spending
        agreementIdToValue[agreementId] = 0;

        }

    }

    function retrieveLINK() public onlyOwner{
        
        // instantiate LINK token
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());

        // transfer remaining contract LINK balance to sender
        require(link.transfer(owner, link.balanceOf(address(this))), "Unable to transfer");
    }


    function escapeHatch() public onlyOwner{
        // for testing purposes, if all gone wrong, retrieve funds
        // to save having to get more from faucets

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




    ////////////////////////////
    // INTERNAL ORACLE REQUEST FUNCS

        function requestDataFromAPI() internal onlyOwner{
        // calls the oracleRequest function with each URL
        // aggregation happens inside fulfill() function

        // require protects against aggregaData ==0 from forgetting to set weights
        require(w1+w2+w3 != 0, "please set weights for aggregating oracle data");
        
        index = 0;
        oracleRequest(APIaddresses[0]);
        oracleRequest(APIaddresses[1]);
        oracleRequest(APIaddresses[2]);
    
    }

    function oracleRequest(string memory url) internal returns (bytes32 requestId) 
    {   
        // oracle request happens here. URL is passed as var url
        // args are jobID, callback address (this contract) and fulfill function from this contract
        Chainlink.Request memory request = buildChainlinkRequest(jobID, address(this), this.fulfill.selector);
        
        // Set the URL to perform the GET request on
        request.add("get", url);
        request.add("path", "data.0.number");
        
        // Sends the request
        return sendChainlinkRequestTo(oracle, request, fee);
    }

    function fulfill(bytes32 _requestId, uint _value) public recordChainlinkFulfillment(_requestId){
        // fulfill will be called 3x, 1x for each call to OracleRequest (via this.fulfill.selector arg)

        // assign data from oracle to position in oracleData array
        oracleData[index] = _value; 
        // iterate through array indexes
        index = index+1; // increment index
        // calculate weighted mean of data in oracleData array
        aggregateData = ((w1*oracleData[0]/100)+(w2*oracleData[1]/100)+(w3*oracleData[2]/100))/3;
    }


    function validateOracleData() internal {    
        // ensures a sufficient number of oracles return valid data
        // avoids accidentally centralizing workflow by relying on 1 oracle

        for (uint16 i = 0; i<oracleData.length; i++) {  //for loop example
            if (oracleData[i] ==0){

                badOracles++;
            } 
        }

    }






    // VIEW FUNCS

    function viewValueFromOracle() public view returns(uint256 viewValue){
        //  show aggregated orace data to user
        viewValue = aggregateData;
    }

    function checkIdForCustomer(address _customer) public view returns(int){
        return(customerToAgreementID[_customer]);
    }

    function checkIdForDonor(address _donor) public view returns(int){
        return(donorToAgreementID[_donor]);
    }

    function checkvalueForAgreementId(int agreementId) public view returns(uint256){
        return(agreementIdToValue[agreementId]);
    }

    function checkDepositAmount() public view returns(uint256 deposit){
        // view function to show user how much DAI was deposited
        deposit = depositedFunds;
    }

    function checkBalance() public view returns (uint256 dai_balance, uint256 adai_balance) {
        
        // balance of DAI and aDAI in contract
        // aDAI is the debt token from the Aave pool
        
        dai_balance = dai.balanceOf(address(this));
        adai_balance = adai.balanceOf(address(this));

    }

    // MODIFIERS AND ACCESSORY FUNCTIONS
    
    modifier onlyOwner(){
        require(owner==msg.sender);
        _;
    }
    
    modifier onlyForValidOracles(){
        require(badOracles<minResponses,"INSUFFICIENT VALID ORACLE RESPONSES: WITHDRAWAL PROHIBITED");
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
