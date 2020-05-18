from web3 import auto # standalone web3 functions and methods
from eth_account import Account # local ethereum wallet functionality
from eth_account.messages import encode_defunct # specific encoding for signing

class Web3Local(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def encrypt_private_key(wallet_private_key, password_hash):

        encrypted_key = Account.encrypt(wallet_private_key, password_hash)
        
        return encrypted_key

    @staticmethod
    def decrypt_private_key(encrypted_key, password_hash):

        wallet_private_key = Account.decrypt(encrypted_key, password_hash)

        return wallet_private_key

    @staticmethod
    def create_private_key():

        import os # for the urandom function to create randomness

        random_string = os.urandom(30).hex() 
        acct = Account.create(random_string)
        wallet_private_key = acct.privateKey.hex()[2:]

        # print(f"New privatekey generated: {wallet_private_key}")
        # print("")

        return wallet_private_key

    @staticmethod
    def get_public_key(wallet_private_key):

        acct = Account.from_key(private_key = wallet_private_key)

        return acct.address

    staticmethod
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

    @staticmethod
    def sign_transaction(txn_dict, wallet_private_key):
          
        # create local account
        acct = Account.from_key(wallet_private_key)

        # sign transaction
        txn_signed = acct.signTransaction(txn_dict)

        return txn_signed

    @staticmethod
    def sign_message(data, wallet_private_key):

        # create local account
        acct = Account.from_key(wallet_private_key)

        # Sign message with the private key
        message = encode_defunct(text=data)
        signed_message = acct.sign_message(message)

        return signed_message

    @staticmethod
    def get_signature(signed_message):

        signature = signed_message['signature'].hex()

        return signature

    @staticmethod
    def get_public_key_from_signature(signature):

        wallet_public_key = Account.recover(signature)

        return wallet_public_key

    @staticmethod
    def create_web3_hash(typearray, valuearray):

        hashbytes = auto.w3.solidityKeccak(abi_types=typearray, values=valuearray)

        return hashbytes

    @staticmethod
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

    @staticmethod
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

if __name__ == '__main__':

    wallet_private_key = Web3Local.create_private_key()
    print(f"wallet private key = {wallet_private_key}")

    wallet_public_key = Web3Local.get_public_key(wallet_private_key)
    print(f"get public key = {wallet_public_key}")

    encrypted_key = Web3Local.encrypt_private_key(wallet_private_key, 1234)
    print(f"encrypted key = {encrypted_key}")

    # Decrypted key is in bytes, but that doesnt change the behavior of signing (in comparison to a plain text private key).
    # the resulting signature is exactly the same
    decrypted_key = Web3Local.decrypt_private_key(encrypted_key, 1234)
    print(f"decrypted key = {decrypted_key}")

    txn_dict = {'value': 0, 'gas': 2000000, 'gasPrice': 10000000000, 'chainId': 3, 'nonce': 75, 'to': '0x87D92d690e4A4E54bA495f94518E452f99f97335', 'data': '0x7e6cc17f000000000000000000000000000000000000000000000000000000000000002000000000000000000000000000000000000000000000000000000000000000062247616e6f6e0000000000000000000000000000000000000000000000000000'}
    txn_signed = Web3Local.sign_transaction(txn_dict, encrypted_key, 1234)
    print(f"txn signed = {txn_signed}")

    message_signed = Web3Local.sign_message("Roy", encrypted_key, 1234)
    print(f"message signed = {message_signed}")