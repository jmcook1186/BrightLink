import React, {useState} from 'react';
import "./App.css";
import Web3 from 'web3'
import background from "./SolarPunkPainting.jpg";
import BrightLink from './artifacts/contracts/BrightLink.json';
import map from "./artifacts/deployments/map.json"

// uses functional component syntax
function App(){

  // web3 is whatever is injected by metamask, else localhost
  // add deployed address for Solidity Storage contract
  const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")
  // define vars and functions to update them, associated to react state
  
  const [account, setOwnerAccount] = useState()
  const [chainID, setChainID] = useState()
  const [network, setNetwork] = useState()
  const [contractAddress, setContractAddress] = useState()
  const [contract, setContract] = useState()
  const[customerAddress, setCustomerAddress] = useState()
  const[donorAddress, setDonorAddress] = useState()
  const [agreementValue, setAgreementValue] = useState()
  const[weight1, setWeight1] = useState()
  const[weight2, setWeight2] = useState()
  const[weight3, setWeight3] = useState()
  const [connected, connect] = useState()


  async function loadBlockChain(){
    
    const chain = await web3.eth.getChainId()
    const net = await web3.eth.net.getNetworkType()
    const accounts = await web3.eth.getAccounts()
    const acc = accounts[0]

    setNetwork(net)
    setChainID(chain)
    setOwnerAccount(acc)

    console.log(chain)
    var address = ''

    if (chain =='1337'){
      address = map["dev"]['BrightLink'][0]
    }
    else if(chain == 42){
      address = map["42"]['BrightLink'][0]
    }
    else if(chain==3){
      address = map["3"]['BrightLink'][0]
    }
    else if(chain==4){
       address = map["4"]['BrightLink'][0]
    }
    else{
      throw 'Please connect to a valid testnet'
    }

    setContractAddress(address)
    const _contract = new web3.eth.Contract(BrightLink.abi, address, account)

    setContract(_contract)
    console.log(address)
    console.log(_contract)
    console.log(chain)
    console.log("contract successfully loaded")
    
    setWeight1(100)
    setWeight2(100)
    setWeight3(100)
    connect(true)
  }



  async function AddNewCustomer(){
   
    await contract.methods.addNewCustomer(customerAddress,donorAddress,agreementValue)
      .send({'from':account})
        .then(console.log("successfully added new customer"))
    
    console.log(customerAddress)
    console.log(donorAddress)
    console.log(agreementValue)
    console.log(typeof(contract))

  }

  async function setBaseLine(){
    await contract.methods.setBaseLine(customerAddress,weight1,weight2,weight3)
      .send({'from':account})
        .then(console.log("successfully set base line"))
  }

  async function getNewData(){
    await contract.methods.UpdateOracleData(customerAddress,weight1,weight2,weight3)
      .send({'from':account})
        .then(console.log("successfully set base line"))
  }

  async function settleAgreement(){
    await contract.methods.settleAgreement(customerAddress)
    .send({'from':account})
      .then(console.log("successfully set base line"))

  }
  

  return (
  
    <div 
    className="App" 
    style={{ backgroundImage: 'url(' + background + ')',
    backgroundPosition: 'center',
    backgroundSize: 'cover',
    backgroundRepeat: 'no-repeat',
    width: '100vw',
    height: '100vh',
    }}>
    
    <h1>BrightLink </h1>

    {<button onClick={loadBlockChain} > Connect Wallet</button>}
    <li style={{ color: 'green'}}>
        {connected? <p><b>connected</b></p> : null}
      </li>

   <p>BrightLink is deployed at: {contractAddress}</p>
   <p>Connected to: {account}</p>
    <br></br>
    <br></br>

    <p><b>Set new agreement</b></p>
    <p><i>(you can only have one active agreement at a time)</i></p>
    <input 
      type="text"
      value={customerAddress}
      placeholder="Set Customer Address"
      onChange={e => setCustomerAddress(e.target.value)} />

    <input 
        type="text"
        value={donorAddress}
        placeholder="Set Donor Address"
        onChange={e => setDonorAddress(e.target.value)} />

    <input
      type="text"
      value={agreementValue}
      placeholder="Set Agreement Value"
      onChange={e => setAgreementValue(e.target.value)} />

    {<button onClick={AddNewCustomer}>Start New Agreement</button>}
    
    <br></br>
    <br></br>

    <p><b>Change satellite weightings and query remote sensing data</b></p>
    <p><i>(please send 0.6 LINK to the contract to fund these queries</i></p>
    <input
      type="text"
      value={weight1}
      placeholder="Set weight for Sentinel (%)"
      onChange={e => setWeight1(e.target.value)} />

    <input
      type="text"
      value={weight2}
      placeholder="Set weight for Landsat (%)"
      onChange={e => setWeight2(e.target.value)} />

    <input
      type="text"
      value={weight3}
      placeholder="Set weight for MODIS (%)"
      onChange={e => setWeight3(e.target.value)} />


    {<button onClick={setBaseLine}>Set Baseline</button>}
    {<button onClick={getNewData}>Get Updated Data</button>}

    <br></br>
    <br></br>
    {<button onClick={settleAgreement}>Request Payout</button>}
    
    </div>

  );
  }


export default App
