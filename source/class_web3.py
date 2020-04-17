import os
import time

from web3 import Web3, auto

from .methods_json import load_json

class Web3Methods(object):
    def __init__(self, w3, contract, account):
        super().__init__()
        self.w3 = w3
        self.contract = contract
        self.account = account
        
    @staticmethod
    def create_private_key():

        random_string = os.urandom(30).hex() 
        accnt = auto.w3.eth.account.create(random_string)
        wallet_private_key = accnt.privateKey.hex()[2:]

        print(f"New privatekey generated: {wallet_private_key}")
        return wallet_private_key

    @staticmethod
    def search_private_key(data):

        try:
            wallet_private_key = data
            print(f"tag has data")

            try:
                auto.w3.eth.account.from_key(wallet_private_key)
                private_key_found = True
                print(f"tag has a valid private key")

            except:
                private_key_found = False
                print(f"no valid private key found on tag")

        except:
            print(f"tag is empty")
            private_key_found = False

        return private_key_found

    @staticmethod
    def faucet(address):
        pass
# >>> transaction = {
#         'to': '0xF0109fC8DF283027b6285cc889F5aA624EaC1F55',
#         'value': 1000000000,
#         'gas': 2000000,
#         'gasPrice': 234567897654321,
#         'nonce': 0,
#         'chainId': 1
#     }
# >>> key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
# >>> signed = w3.eth.account.signTransaction(transaction, key)

# >>> signed.rawTransaction
# HexBytes('0xf86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428')
# >>> signed.hash
# HexBytes('0xd8f64a42b57be0d565f385378db2f6bf324ce14a594afc05de90436e9ce01f60')
# >>> signed.r
# 4487286261793418179817841024889747115779324305375823110249149479905075174044
# >>> signed.s
# 30785525769477805655994251009256770582792548537338581640010273753578382951464
# >>> signed.v
# 37

# # When you run sendRawTransaction, you get back the hash of the transaction:
# >>> w3.eth.sendRawTransaction(signed.rawTransaction) 


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

    def initialize_contract(self, abi, contract_address="", solidity="", bytecode=""):

        if contract_address == "" and bytecode == "" and solidity == "":

            print("provide valid contract address, solidity contract or bytecode to create a new contract!")

        else:

            if bytecode != "":
                # if bytecode is provided, create new contract (address) with provided bytecode
                contract_address = self.init_deploy_bytecode(abi, bytecode)

            elif solidity != "":
                # if solidity contract is provided, create new contract (address) with provided contract
                contract_address = self.init_deploy_solidity(abi, solidity)   
            
            # Setting up contract with the needed abi (functions) and the contract address (for instantiation)
            abi = load_json(abi["path"], abi["file"])
            # print(abi)
            
            self.contract = self.w3.eth.contract(abi = abi, address = contract_address)
            print(f"Connected to ethereum smart contract: {self.contract.address}")

    def init_deploy_solidity(self, abi, solidity):
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

    def init_deploy_bytecode(self, abi, bytecode):
        """deploying a new contract with abi and bytecode"""

        # getting bytecode by opening the bytecode text file and save it as a string
        with open(bytecode, mode='r') as infile:
            bytecode = infile.read()

        # set up the contract based on the bytecode and abi functions
        contract = self.w3.eth.contract(abi = abi, bytecode = bytecode)

        # construct transaction
        txn_construct = contract.constructor().buildTransaction({
            'from': self.account.address,
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
            'gasPrice': self.w3.toWei('10000000000', 'wei'),
            'chainId': 3, 
            }
        )
        # print(f"Constructed transaction: {txn_construct}") # Shows huge bit string

        # sign transaction
        txn_signed = self.account.signTransaction(txn_construct)
        # print(f"Signed transaction: {txn_signed}") # Shows huge bit string

        # send transaction
        txn_hash = self.w3.eth.sendRawTransaction(txn_signed.rawTransaction)
        print(f"Transaction send with hash: {txn_hash.hex()}")

        # wait for processing
        print("waiting for nodes to handle txn")
        time.sleep(60)

        # request receipt
        txn_receipt = self.w3.eth.getTransactionReceipt(txn_hash.hex())
        print(f"Requested receipt: {txn_receipt}")

        # return new contract address
        new_contract_address = txn_receipt["contractAddress"]
        print(f"New contract address: {new_contract_address}\n")

        return new_contract_address

    def create_character(self, name, unit, race):

        # get nonce for txn input
        nonce = self.w3.eth.getTransactionCount(self.account.address)

        # get identifier for function input
        identifier = f"{name} - {unit} - {race}"

        # build transaction
        txn_dict = self.contract.functions.createRandomCharacter(
            identifier, 
            name, 
            unit, 
            race
            ).buildTransaction({
            'nonce': nonce,        
            'gas': 1648900,
            'gasPrice': self.w3.toWei('1000000000', 'wei'),
            'chainId': 3,
            })
        print("build txn dict: " + str(txn_dict))

        # sign transaction
        txn_signed = self.account.signTransaction(txn_dict)
        # print(f"Signed transaction: {txn_signed}") # Shows huge bit string

        # send transaction
        txn_hash = self.w3.eth.sendRawTransaction(txn_signed.rawTransaction)
        print(f"Transaction send with hash: {txn_hash.hex()}")

        # wait for processing
        print("waiting for nodes to handle txn")
        time.sleep(60)

        # request receipt
        txn_receipt = self.w3.eth.getTransactionReceipt(txn_hash.hex())
        print(f"Requested receipt: {txn_receipt}")

        # return creation of character
        newcharacter = f"added {name} a {unit} consist of {race}"

        return newcharacter

    def create_event(self, characterId, description):
        """create an event for a specific character by sending input to the smart contract of cryptocharacter"""
        # get nonce for txn input
        nonce = self.w3.eth.getTransactionCount(self.account.address)

        # construct transaction
        txn_dict = self.contract.functions.createEvent(
            characterId, 
            description
            ).buildTransaction({
            'nonce': nonce,        
            'gas': 1648900,
            'gasPrice': self.w3.toWei('1000000000', 'wei'),
            'chainId': 3,
            })
        # print(f"Constructed transaction: {txn_construct}") # Shows huge bit string

        # sign transaction
        txn_signed = self.account.signTransaction(txn_dict)
        # print(f"Signed transaction: {txn_signed}") # Shows huge bit string

        # send transaction
        txn_hash = self.w3.eth.sendRawTransaction(txn_signed.rawTransaction)
        print(f"Transaction send with hash: {txn_hash.hex()}")

        # wait for processing
        print("waiting for nodes to handle txn")
        time.sleep(60)

        # request receipt
        txn_receipt = self.w3.eth.getTransactionReceipt(txn_hash.hex())
        print(f"Requested receipt: {txn_receipt}")

        # return created event
        newevent = f"Added event for {characterId}: {description}"

        return newevent

    def get_characters(self):
        # print all knwon characters of the given wallet_address
        characters = self.contract.functions.getCharactersByOwner(self.account.address).call()

        characterlist = []
        for i in characters:
            charlist = self.contract.functions.characters(i).call()
            idlist = [i]
            character = idlist + charlist
            characterlist += [character]

        return characterlist

    def get_events(self, characterId):
        """get all events for a specific character by sending input to the smart contract of cryptocharacter"""

        # get all knwon events of the given character
        events = self.contract.functions.getEventsByCharacter(characterId).call()

        history = []
        history += ["characterId: " + str(characterId)]
        for i in events:
            eventlist = self.contract.functions.events(i).call()
            idlist = [i]
            event = idlist + [eventlist]
            history += [event]

        return history