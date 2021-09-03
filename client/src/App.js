import React, {useState} from 'react';
import "./App.css";
import Web3 from 'web3'
import BrightLink from '/home/joe/Code/BrightLink/client/src/artifacts/contracts/BrightLink.json';
const BrightLinkAddress = '0xa442852B9B9A92B277E6aF0FDcAe986EAa1986B3'



function App (){

const [account, setOwnerAccount] = useState()
const [customerAddress, setCustomerAddress] = useState()
const [donorAddress, setDonorAddress] = useState()
const [agreementValue, setAgreementValue] = useState()
const [network, setNetwork] = useState()
var connected = false;

async function loadBlockchainData(){
  
  const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")
  const network = await web3.eth.net.getNetworkType()
  console.log("You are connected to the **", network, "** network")
  const accounts = await web3.eth.getAccounts()
  setOwnerAccount(accounts[0])
  console.log("account = ", account)
  setNetwork({network})
  connected = true
}


async function AddNewCustomer(){
  
  const web3 = new Web3(Web3.givenProvider || "http://localhost:8545")
  const contract = new web3.eth.Contract(BrightLink.abi, BrightLinkAddress, account)
  
  await contract.methods.addNewCustomer(customerAddress,donorAddress,agreementValue).send({'from':account}).then(console.log("success"))
  
  console.log(customerAddress)
  console.log(donorAddress)
  console.log(agreementValue)
  console.log(typeof(contract))

}

return (
  <div className="App">
  <header className="App-header"></header>
  
  <br></br>
  {<button onClick={loadBlockchainData}>Connect Wallet</button>}
  <br></br>
  {connected ? <p>wallet connected</p>: <p></p>}
  <br></br>

  <input onChange={e => setCustomerAddress(e.target.value)} placeholder="Set Customer Address" />
  <input onChange={e => setDonorAddress(e.target.value)} placeholder="Set Donor Address" />
  <input onChange={e => setAgreementValue(e.target.value)} placeholder="Set Agreement Value" />

  <br />
  {<button onClick={AddNewCustomer}>Start New Agreement</button>}

</div>
);
}


export default App
