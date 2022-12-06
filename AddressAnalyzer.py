from pprint import pprint
import sys
import re
import requests
import os
import subprocess
from dotenv import load_dotenv
import web3
from web3 import Web3

# Create a dictionary that maps common method names to different types of smart contracts
METHODS_DICT = {
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
        # The command to run the decompiler
        decompiler_command = f"panoramix {self.address}"

        # Split the command into a list of arguments
        decompiler_args = decompiler_command.split()
        
        # The first argument is the program name
        program = decompiler_args[0]

        # The second argument is the contract address
        contract_address = decompiler_args[1]

        # Run the decompiler and capture the output
        decompiler_output = subprocess.run([program, contract_address], stdout=subprocess.PIPE).stdout.decode("utf-8")
        
        # Remove the ANSI escape codes
        decompiler_output = re.sub(r"\x1b\[[0-9;]*m", "", decompiler_output)
        
        # Use regular expressions to search for lines that contain "def" followed by the method name
        methods = re.findall(r"def (\w+):?", decompiler_output)

        # Set baseurl for RESTful api request
        baseurl = "https://www.4byte.directory/api/v1/signatures/?hex_signature="
        
        # Init a dict
        methods_dict = {}
        # Iterate over the list of current methods with indexing
        for idx, method in enumerate(methods):
            # Check if decompiler returned unknown methods 
            if 'unknown' in method:
                # Remove the string "unknown", remaining is function hex signature
                methods[idx] = method[7:]
                hex_signature = methods[idx]
                
                # API get request to retreive the actual name based on the hex signature
                value = AddressAnalyzer.parse_json(AddressAnalyzer.main_request(baseurl + hex_signature))
                
                # Dict mapping the hex and name respectivly
                methods_dict[hex_signature] = value

                # Update the list
                methods[idx] = value
            else:
                methods_dict[methods[idx]] = method

        # Flatten the method list as the RESfulAPI hex signature 
        # sometimes returns multiple methods corresponding to a single hex
        # e.g - flattens list of lists to a normal list
        flatten_methods = []
        for method in methods:
            if type(method) is str:
                flatten_methods.append(method)
            else:
                flatten_methods.extend(method)
        
        # Initialize an empty list to store the probable contract types
        probable_types = []
        # Iterate over the list of methods in the contract        
        for method in flatten_methods:
            # Get only the name of the method without the arguments
            name = re.sub(r'\(.*\)', '', method)
            # Check if the method name is in the dictionary
            if name in METHODS_DICT:
                # If a match is found, add the corresponding contract type to the list
                probable_types.append(METHODS_DICT[name])

        return probable_types

    
    def main_request(request):
        # api request to baseurl = "https://www.4byte.directory/api/v1/signatures/?hex_signature="
        r = requests.get(request, verify=False)
        return r.json()


    def parse_json(response):
        result = [] 
        for item in response['results']:
        # print(item)
            result.append(item['text_signature'])

        return result



# Create an instance of the AddressAnalyzer class
analyzer = AddressAnalyzer(sys.argv[1])

# Check if the address is an EOA
if analyzer.is_eoa():
    print("The address is an EOA.")
else:
    # Get the probable type of the smart contract
    contract_type = analyzer.get_contract_type()
    print("The address is a smart contract of type: ", contract_type)








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

