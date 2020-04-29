import os
import time

from web3 import Web3, auto

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

        # Connect to specific network
        w3 = Web3(Web3.HTTPProvider(network_url))
        print(f"Connected to ethereum node {network_url}: {w3.isConnected()}")

        return Web3Connection(w3)

    def initialize_wallet(self, wallet_private_key):

        # account to interact from
        self.account = self.w3.eth.account.privateKeyToAccount(wallet_private_key)
        print(f"Connected with key belonging to {self.account.address}")
        print("")

    def initialize_contract(self, abi, contract_address="", solidity="", bytecode=""):

        if contract_address != "":
            pass

        elif bytecode != "":
            # if bytecode is provided, create new contract (address) with provided bytecode
            contract_address = self.create_txn_contract_bytecode(abi, bytecode)

        elif solidity != "":
            # if solidity contract is provided, create new contract (address) with provided contract
            contract_address = self.create_txn_contract_solidity(abi, solidity)   

        else:
            print("provide valid contract address or provide a solidity or bytecode to create a new contract!")

        # Setting up contract with the needed abi (functions) and the contract address (for instantiation) 
        self.contract = self.w3.eth.contract(abi = abi, address = contract_address)
        print(f"Connected to ethereum smart contract: {self.contract.address}")

    def create_txn_contract_solidity(self, abi, solidity):
        NotImplemented
        return contract_address
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
        """deploying a new contract with abi and bytecode"""

        # getting bytecode by opening the bytecode text file and save it as a string
        # with open(bytecode, mode='r') as infile:
        #     bytecode = infile.read()

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

        # return new contract address
        new_contract_address = txn_receipt["contractAddress"]
        print(f"New contract address: {new_contract_address}\n")

        return new_contract_address

    def create_txn_transfer(self, to_address, value):
        
        print("Trying to transfer ETH")
        
         # get the transaction default values (gasprice, chainid, gas)
        txn_dict_build = transaction_dictionary_defaults()
        txn_dict_build.update({
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'to': to_address,
            'value': value,
            })

        txn_dict = txn_dict_build
        txn_hash = self.send_transaction(txn_dict)

        print(f"Deposited {value} Eth in this account")
        print("")

        return txn_hash

    def get_nonce(self):
        nonce = self.w3.eth.getTransactionCount(self.account.address)
        return nonce

    def send_transaction(self, txn_dict):
        
        # sign transaction
        txn_signed = self.account.signTransaction(txn_dict)
        # print(f"Signed transaction: {txn_signed}") # Shows huge bit string

        # send transaction
        txn_hash = self.w3.eth.sendRawTransaction(txn_signed.rawTransaction)
        print(f"Transaction send with hash: {txn_hash.hex()}")

        # request receipt
        status = "Waiting for receipt"
        while status == "Waiting for receipt":
            try:
                txn_receipt = self.w3.eth.getTransactionReceipt(txn_hash.hex())
                status = f"Confirmed with receipt: {txn_receipt}"
                print(status)
            except:
                print(status)
                time.sleep(1)
        
        print("Waiting a bit to make sure the transaction completed")
        time.sleep(5)

        return txn_receipt