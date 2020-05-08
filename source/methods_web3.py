import os
import time

from web3 import auto
from web3 import Web3

def create_private_key():

    random_string = os.urandom(30).hex() 
    account = auto.w3.eth.account.create(random_string)
    wallet_private_key = account.privateKey.hex()[2:]

    # print(f"New privatekey generated: {wallet_private_key}")
    # print("")

    return wallet_private_key

def search_private_key(data):

    try:
        wallet_private_key = data
        # print(f"tag has data {data}")

        try:
            auto.w3.eth.account.from_key(wallet_private_key)
            private_key_found = True
            # print(f"tag has a valid private key")
            # print("")

        except:
            private_key_found = False
            # print(f"no valid private key found on tag")

    except:
        # print(f"tag is empty")
        private_key_found = False

    return private_key_found

def transaction_dictionary_defaults():
    """nonce is mandatory, others are optional, if gas = 0 then the default will be used."""
    
    txn_build_dict = {
        "gas": 2000000,
        "gasPrice": auto.w3.toWei("10000000000", "wei"),
        "chainId": 3,
        }

    # contract constructor uses nonce, chainid, gasprice, from
    # function execute uses nonce, chainid, gasprice, gas, 
    # transfer uses nonce, chainid, gasprice, gas, to, value, 

    return txn_build_dict

def deploy_dictionary_defaults():
    """nonce is mandatory, others are optional, if gas = 0 then the default will be used."""
    
    txn_build_dict = {
        "gasPrice": auto.w3.toWei("10000000000", "wei"),
        "chainId": 3,
        }

    # contract constructor uses nonce, chainid, gasprice, from
    # function execute uses nonce, chainid, gasprice, gas, 
    # transfer uses nonce, chainid, gasprice, gas, to, value, 

    return txn_build_dict