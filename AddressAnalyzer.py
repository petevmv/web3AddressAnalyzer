import re
import os
import subprocess
from dotenv import load_dotenv
import web3
from web3 import Web3

load_dotenv()

# Set Provider
w3 = Web3(
    Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI"))
)

class AddressAnalyzer:
    def __init__(self, address):
        self.address = address
    
    def is_eoa(self):
        # Check if the address is an EOA
        # Return True if it is an EOA, False if it is a smart contract
        if Web3.toInt(w3.eth.get_code(Web3.toChecksumAddress(self.address))) == 0:
            return True
        
        return False
    
    def get_contract_type(self):
        # Use an open source decoder or decompiler to decode the smart contract
        # Get the methods in the contract and compare them to samples of real world
        # smart contracts to determine the probable type of the contract
        # Return the probable type of the contract
        pass


EOA = '0xC43c0001501047b6DC2721b78c3C2268b583995d'

# Create an instance of the AddressAnalyzer class
analyzer = AddressAnalyzer(EOA)

# Check if the address is an EOA
if analyzer.is_eoa():
    print("The address is an EOA.")
else:
    # Get the probable type of the smart contract
    contract_type = analyzer.get_contract_type()
    print("The address is a smart contract of type: ", contract_type)





# Create a dictionary that maps common method names to different types of smart contracts
methods_dict = {
    "transfer": "ERC20",
    "balanceOf": "ERC20",
    "approve": "ERC20",
    "transferFrom": "ERC20",
    "allowance": "ERC20",
    "totalSupply": "ERC20",
    "mint": "ERC20",
    "burn": "ERC20",
    "payable": "ERC20",
    "send": "ERC20",
    "deposit": "ERC20",
    "withdraw": "ERC20",
    "addLiquidity": "Uniswap",
    "removeLiquidity": "Uniswap",
    "getPrice": "Uniswap",
    "getInputPrice": "Uniswap",
    "swapExactTokensForTokens": "Uniswap",
    "swapTokensForExactTokens": "Uniswap",
}

# Initialize an empty list to store the probable contract types
probable_types = []
methods = []
# Iterate over the list of methods in the contract
for method in methods:
    # Check if the method name is in the dictionary
    if method in methods_dict:
        # If a match is found, add the corresponding contract type to the list
        probable_types.append(methods_dict[method])

# Print the list of probable contract types
print(probable_types)

