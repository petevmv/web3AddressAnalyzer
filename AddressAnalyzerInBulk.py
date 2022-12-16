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
    "mint": "ERC20, DAO, liquidity pool",
    "burn": "ERC20, liquidity pool",
    "payable": "ERC20",
    "send": "ERC20",
    "deposit": "ERC20",
    "withdraw": "ERC20",
    "addLiquidity": "liquidity pool",
    "removeLiquidity": "liquidity pool",
    "getPrice": "Uniswap",
    "getInputPrice": "DEX, Uniswap",
    "swapExactTokensForTokens": "DEX, Uniswap",
    "swapTokensForExactTokens": "DEX, Uniswap",
    "addToAllowedList":'TornadoCash',
    "bulkResolve": 'TornadoCash',
    "changeTransferability": "TornadoCash",
    "getGovernance": "TornadoCash",
    "getSignature": "TornadoCash",
    "stake": "staking and liquidity pool",
    "unstake": 'staking and liquidity pool',
    "getTotalEarnedAmount": 'staking and liquidity pool',
    "addToAprLockOption": 'staking and liquidity pool',
    "borrow" : 'Loan, Lending',
    "repay" : 'Loan, Lending',
    "liquidate" : 'Loan, Lending',
    "setLoanParams" : "Loan, Lending",
    "setCollateralParams" : 'Loan, Lending',
    "ownerOf" : "ERC721, ERC1155",
    "safeTransferFrom" : "ERC721",
    "batchTransfer" : "ERC1155",
    "propose" : "DAO",
    "vote" : "DAO, govtoken",
    "delegate": "liquidity pool",
    "delegateBySig" : 'liquidity pool',
    "whitelistInvestor" : "ICO",
    "registerInvestor" : "ICO",
    "mintTokens" : "ICO",
    "InitializableAdminUpgradeabilityProxy": "type AAVE",
    "admin" : 'type AAVE',
    "upgradeTo": "type AAVE",
    "upgradeToAndCall" : 'type AAVE'
}


load_dotenv()

with open('to_analize.txt') as file:
    addresses = eval(file.read())


# list_of_addresses = ["0xC43c0001501047b6DC2721b78c3C2268b583995d",'0x55a6d9fbaebb268dc2fd94bed6c156bc82184004']

class AddressAnalyzerInBulk:
    def __init__(self, envvar):
        # Set Provider
        self.w3 = Web3(
            Web3.HTTPProvider(os.getenv(envvar))
                )       
        
    def is_eoa(self, address):
        # Check if the address is an EOA
        # Return True if it is an EOA, False if it is a smart contract
        if Web3.toInt(self.w3.eth.get_code(Web3.toChecksumAddress(address))) == 0:
            return True
        
        return False
    
    def get_SC_and_EOAs(self, addresses):
        # init lists for smart contracts and EOA's
        EOAs = []
        SC = []
        # iterate over the passed addresess and populate the respective lists
        for address in addresses:
            if self.is_eoa(address):
                EOAs.append(address)
            else:
                SC.append(address)
        
        return (SC, EOAs)


    def decompile(self, contract_address):
        # The command to run the decompiler
        decompiler_command = f"panoramix {contract_address}"

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

        return decompiler_output

# get_methods(self.decompile(contract_address))
    def get_methods(output):
        # Use regular expressions to search for lines that contain "def" followed by the method name
        methods = re.findall(r"def (\w+):?", output)

        # Set baseurl for RESTful api request
        baseurl = "https://www.4byte.directory/api/v1/signatures/?hex_signature="

        # Iterate over the list of current methods with indexing
        for idx, method in enumerate(methods):
            # Check if decompiler returned unknown methods 
            if 'unknown' in method:
                # Remove the string "unknown", remaining is function hex signature
                methods[idx] = method[7:]
                hex_signature = methods[idx]
                                
                # API get request to retreive the actual name based on the hex signature
                value = AddressAnalyzerInBulk.parse_json(AddressAnalyzerInBulk.main_request(baseurl + hex_signature))
                

                # Update the list               
                methods[idx] = value
        
        flattend_methods = []
        for method in methods:
            if type(method) is str:
                flattend_methods.append(method)
            else:
                flattend_methods.extend(method)


        
        return flattend_methods
    
    def get_contract_type(self, addresses):
        pass
    

    def methods_intersection(self, addresses):
        # get only the smart contracts as list
        smart_conrtact_list = self.get_SC_and_EOAs(addresses)[0]

        list_methods = []
        # iterate over the SC list to decompile and capture methods
        for contract in smart_conrtact_list:
            decompile_output = self.decompile(contract)
            methods = AddressAnalyzerInBulk.get_methods(decompile_output)
            # append as sets data structure with the idea to use set.intersection
            list_methods.append(set(methods))

        result = set.intersection(*list_methods)
        return result
    
    def create_or_update_data(set_of_methods):
        dict_type = {}
        lend_keywords = ['borrow', 'repay','liquidate']
        for method in set_of_methods:
            for key in lend_keywords:
                if key in method.lower()
                    pass
                    # dict_type['Lending'] = 

   
  
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
analyzer = AddressAnalyzerInBulk("WEB3_PROVIDER_URI")



print(analyzer.methods_intersection(addresses))


# "WEB3_PROVIDER_URI" 