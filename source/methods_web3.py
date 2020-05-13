from web3 import auto # standalone web3 functions and methods

def create_private_key():

    import os # for the urandom function to create randomness

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

def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """
    import platform    # For getting the operating system name
    import subprocess  # For executing a shell command

    index = host.find("//")
    if index != -1:
        i = index + 2
        host = host[i:]
    
    index = host.find(":")
    if index != -1:
        host = host[:index]
        
    # Option for the number of packets as a function of
    param = '-n' if platform.system().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    subprocess.call(command)

if __name__ == '__main__':

    ping("http://192.168.178.25:8545")