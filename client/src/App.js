import React, {useEffect, useState} from 'react';
import "./App.css";
import Web3 from 'web3'
import background from "./TreeBorder2.jpg";
import BrightLink from './artifacts/contracts/BrightLink.json';
import map from "./artifacts/deployments/map.json";
import {getEthereum} from "./getEthereum"

// uses functional component syntax
function App(){

  const [account, setOwnerAccount] = useState()
  const [chainID, setChainID] = useState()
  const [network, setNetwork] = useState()
  const [contractAddress, setContractAddress] = useState()
  const [contract, setContract] = useState()
  const[customerAddress, setCustomerAddress] = useState()
  const[donorAddress, setDonorAddress] = useState()
  const [agreementValue, setAgreementValue] = useState()
  const [connected, connect] = useState()
  const[ndvi, set_ndvi] = useState()

  
  // loadBlockChain detects metamask account
  // and network ID 
  async function loadBlockChain(){

    const ethereum = await getEthereum()
    let web3

    if (ethereum) {
        web3 = new Web3(ethereum)
    } else if (window.web3) {
        web3 = window.web3
    } else {
        const provider = new Web3.providers.HttpProvider(
            "http://127.0.0.1:8545"
        );
        web3 = new Web3(provider)
    }

    

    // // Try to enable accounts (connect metamask)
    // const ethereum = await getEthereum()
    const accounts = await ethereum.request({method:'eth_requestAccounts'})
    const chain = await web3.eth.getChainId()
    const net = await web3.eth.net.getNetworkType()

    //const accounts = await web3.eth.getAccounts()
    const acc = accounts[0]
    console.log("connected account: " + acc)

    setNetwork(net)
    setChainID(chain)
    setOwnerAccount(acc)

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
    const _contract = new web3.eth.Contract(BrightLink.abi, address, acc)
    
    setContract(_contract)
    console.log("address: " + address)
    console.log("contract:  " + _contract.methods)
    console.log("chain: " + chain)
    console.log("contract successfully loaded")
    
    set_ndvi(0)

    if (account){
      connect(true)

    }

    web3.eth.Contract.defaultAccount = account

    return web3, contract, ethereum
  }



  async function AddNewCustomer(){

    await contract.methods.addNewCustomer(customerAddress,donorAddress, agreementValue)
      .send({'from':account})
        .then(console.log("successfully added new customer"))
    
    console.log(customerAddress)
    console.log(donorAddress)
    console.log(agreementValue)
    console.log(typeof(contract))

  }

  async function setBaseLine(){
    await contract.methods.setBaseLine(customerAddress)
      .send({'from':account})
        .then(console.log("initial data successfully obtained from oracle"))
  }

  async function getNewData(){
    let _customerAddress = String(customerAddress)
    await contract.methods.UpdateOracleData(_customerAddress)
      .send({'from':account})
      console.log("updated data successfully obtained from oracle")
  }

  async function settleAgreement(){
    let _customerAddress = String(customerAddress)
    await contract.methods.settleAgreement(_customerAddress)
    .send({'from':account})
    console.log("the contract has paid DAI to either the customer or donor")

  }
  
  async function viewNDVIdata(){
    let a = await contract.methods.viewValueFromOracle().call()
    set_ndvi(a)
    
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

    <li style={{position:"absolute",right:5, bottom: 30, color: 'black'}}>
    <a href="https://github.com/Yeti87803643/blockchain-developer-bootcamp-final-project"><b>Documentation</b></a>
    </li>

    <br></br>
    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <h1>BrightLink </h1>
    </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <h2>Incentivized urban greening validated by satellite data</h2>
    </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    {<button onClick={loadBlockChain} > Connect Wallet</button>}
    </li>
      
    <li style={{position:"absolute",left:5, top: 5, color: 'green'}}>
    {connected? <p><b>CONNECTED!</b></p> : null}
    </li>

    <li style={{position:"absolute",left:5, top: 30, color: 'black'}}>
    <p>Contract is deployed at:</p> <p>{contractAddress}</p>
    </li>

    <li style={{position:"absolute",left:5, top: 100, color: 'black'}}>
    <p>Connected to account:</p><p>{account}</p>
    </li>

      
    <br></br>
    <br></br>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <p><h3>Start new project </h3></p>
    </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
      <p>Customer (Ethereum address)&nbsp;&nbsp;&nbsp;&nbsp;</p>

    <input 
      type="text"
      value={customerAddress}
      placeholder="Set Customer Address"
      onChange={e => setCustomerAddress(e.target.value)} />
      </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <p>Donor (Ethereum address)&nbsp;&nbsp;&nbsp;&nbsp;</p>

    <input 
        type="text"
        value={donorAddress}
        placeholder="Set Donor Address"
        onChange={e => setDonorAddress(e.target.value)} />
    </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <p>Funding Value (Dai)&nbsp;&nbsp;&nbsp;&nbsp;</p>

    <input
      type="text"
      value={agreementValue}
      placeholder="Set Funding Value"
      onChange={e => setAgreementValue(e.target.value)} />
    </li>
    <br></br>
    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    {<button onClick={AddNewCustomer}>CONFIRM</button>}
    </li>

    <br></br>
    <br></br>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    <p><b>Query Satellite data</b></p>

    </li>
    <br></br>
 
    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    {<button onClick={setBaseLine}>Set Baseline</button>}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    {<button onClick={getNewData}>Get Updated Data</button>}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    {<button onClick={settleAgreement}>Request Payout</button>}
    </li>

    <li style={{display: 'flex', justifyContent:'center', alignItems:'center', color: 'black'}}>
    {<button onClick={viewNDVIdata}>View NDVI data</button>}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<p> vegetation coverage: {ndvi} %</p>
    </li>



    </div>

  );
  }


export default App
