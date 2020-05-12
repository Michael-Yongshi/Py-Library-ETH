import os
import time

from web3 import Web3, auto
from eth_account.messages import encode_defunct

from .methods_web3 import (
    create_private_key,
    search_private_key,
    transaction_dictionary_defaults,
    deploy_dictionary_defaults,
)
from .methods_json import load_json

class Web3Connection(object):
    def __init__(self, w3, account = None, contract = None):
        super().__init__()
        self.w3 = w3
        self.account = account
        self.contract = contract

    @staticmethod
    def initialize_connection(network_url):
        """Initialize a Web3 connection to the given node at a certain url
        returns the connection if it executes successfully"""

        # Connect to specific network
        try:
            w3 = Web3(Web3.HTTPProvider(network_url))
            if w3.isConnected() == True:
                print(f"Success: Web3 connection to ethereum node {network_url}")
            else:
                print(f"Failed to create a Web3 connection to ethereum node {network_url}")
            return Web3Connection(w3)
        except:
            print(f"FAILED TO SET UP WEB3 CONNECTION TO NODE {network_url}")

    def initialize_wallet(self, wallet_private_key):
        """initializes a wallet from a given private key
        Returns the wallet address if it is successfully executed, otherwise an error message."""

        # Connect to account
        try:
            self.account = self.w3.eth.account.privateKeyToAccount(wallet_private_key)
            wallet_address = self.account.address
            print(f"Success: Web3 connection to wallet at {wallet_address}")
            return wallet_address
        except:
            print(f"FAILED TO CONNECT TO WALLET WITH PRIVATE KEY {wallet_private_key}")

    def initialize_contract(self, abi, contract_address="", solidity="", bytecode=""):
        """Initializes a connection with a contract, if necessary it deploys it.
        Returns the contract address if it is successfully executed, otherwise an error message."""

        # try:
        if bytecode != "":
            # if bytecode is provided, create new contract (address) with provided bytecode
            txn_receipt = self.create_txn_contract_bytecode(abi, bytecode)
            contract_address = txn_receipt['contractAddress']
        elif solidity != "":
            return f"Solidity Contract deployment is not implemented"
            # if solidity contract is provided, create new contract (address) with provided code
            # contract_address = self.create_txn_contract_solidity(abi, solidity)   
        elif contract_address != "":
            # If contract address is provided, connect to existing contract (no deployment required)
            pass
        else:
            return f"Provide valid contract address, solidity code or bytecode input"

        # Initialize connection
        self.contract = self.w3.eth.contract(abi = abi, address = contract_address)
        
        print(f"Success: Web3 connection to smart contract at {contract_address}")

        return self.contract.address

        # except:
        #     return f"FAILED TO CONNECT TO SMART CONTRACT WITH CONTRACT ADDRESS {contract_address}, SOLIDITY CODE {solidity} OR BYTECODE {bytecode}"

    def create_txn_contract_solidity(self, abi, solidity):
        NotImplemented
        # relative_path = os.path.join("source", solidity)
        # current_directory = os.path.dirname(os.path.dirname(__file__))
        # absolute_path = os.path.join(current_directory, relative_path)

        # print(f"relative path {relative_path}")
        # print(f"absolute path {absolute_path}")

        # compile standard
        # compiled_sol = compile_standard(
        #     {"sources": absolute_path}
        # )

        # compile directly a sol file
        # compiled_sol = compile_files(absolute_path)

        # compile solidity source code
        # with open(relative_path, mode='r') as infile:
        #     source = infile.read()
        # compiled_sol = compile_source('pragma solidity ^0.4.0; contract A{ funcion A() public{}}')

    def create_txn_contract_bytecode(self, abi, bytecode):
        """deploying a new contract with supplied abi and bytecode
        Returns the contract address if it is successfully executed."""

        # set up the contract based on the bytecode and abi functions
        contract = self.w3.eth.contract(abi = abi, bytecode = bytecode)

        # get the transaction default values (gasprice, chainid, gas)
        txn_dict_build = deploy_dictionary_defaults()
        txn_dict_build.update({
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            })

        # construct transaction
        txn_dict = contract.constructor().buildTransaction(txn_dict_build)

        # send transaction
        txn_receipt = self.send_transaction(txn_dict)
        txn_hash = txn_receipt['transactionHash'].hex()
        txn_contract_address = txn_receipt['contractAddress']
        if txn_receipt["status"] == 1:
            print(f"Success: Web3 created new contract at {txn_contract_address} with hash {txn_hash}")
        else:
            print(f"Failed: Deploy contract transaction reverted with hash {txn_hash}")

        return txn_receipt

    def create_txn_transfer(self, to_address, value):
        """Creates a transaction dict to transfer ETH of supplied value to the supplied to-address. 
        Returns the hash if it is successfully executed."""

         # get the transaction default values (gasprice, chainid, gas)
        txn_dict_build = transaction_dictionary_defaults()
        txn_dict_build.update({
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'to': to_address,
            'value': value,
            })

        txn_dict = txn_dict_build
        txn_receipt = self.send_transaction(txn_dict)
        txn_hash = txn_receipt['transactionHash'].hex()

        if txn_receipt["status"] == 1:
            print(f"Success: Send ETH of value {value} to {to_address} with hash {txn_hash}")
        else:
            print(f"Failed: Send ETH transaction reverted with hash {txn_hash}")
        
        return txn_receipt

    def get_nonce(self):
        """Get the nonce for a new transaction for this account
        Returns the nonce if it is successfully executed."""

        nonce = self.w3.eth.getTransactionCount(self.account.address)
        return nonce

    def send_transaction(self, txn_dict):
        """Creates a transaction of the supplied transaction dict and sends it. 
        Returns the hash if it is successfully executed."""

        # sign transaction
        txn_signed = self.account.signTransaction(txn_dict)
        # print(f"Signed transaction: {txn_signed}") # Shows huge bit string

        # send transaction
        txn_hash = self.w3.eth.sendRawTransaction(txn_signed.rawTransaction)

        # request receipt
        status = "Waiting for receipt"
        while status == "Waiting for receipt":
            try:
                txn_receipt = self.w3.eth.getTransactionReceipt(txn_hash.hex())
                status = f"Receipt confirmed!"
                print(f"--{status}--")
            except:
                print(f"--{status}--")
                time.sleep(10)
        
        # Making sure transaction went through (otherwise you get a replacement error)
        time.sleep(5)

        # print(txn_receipt)
        return txn_receipt

    def sign_message(self, data, wallet_private_key):

        message = encode_defunct(data)
        signed_message = auto.w3.eth.account.sign_message(message, wallet_private_key)
        signature = signed_message['signature'].hex()

        return signature

    def hash_message(self, typearray, valuearray):

        hashbytes = self.w3.solidityKeccak(abi_types=typearray, values=valuearray)

        return hashbytes