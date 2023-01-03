import json
import pandas as pd
import csv
from pprint import pprint
import re
import requests
import os
import subprocess
from dotenv import load_dotenv
import web3
from web3 import Web3



load_dotenv()

# Opens the file that contains addresses to be analized and store them var addresses
with open('to_analize.txt') as file:
    addresses = eval(file.read())


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
        # Init lists for smart contracts and EOA's
        EOAs = []
        SC = []
        # Iterate over the passed addresess and populate the respective lists
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
        
        # flatten the methods list from [[],[]...] to [] as the API returns list structure 
        flattend_methods = []
        for method in methods:
            if type(method) is str:
                flattend_methods.append(method)
            else:
                flattend_methods.extend(method)
        
        return flattend_methods
    
    def get_contract_type(self, addresses):
        # get only the smart contracts as list
        smart_conrtact_list = self.get_SC_and_EOAs(addresses)[0]
    
        excluded_methods = {'_fallback', 'storage', 'name'}        

        list_methods = []
        # opnes the file .csv and write to it(if 'a' is passed - it appends, if 'w' -  writes )
        with open('analized.csv', 'w') as file:
            for contract in smart_conrtact_list:
                decompiler_output = self.decompile(contract)
                methods = AddressAnalyzerInBulk.get_methods(decompiler_output)
                writer = csv.writer(file)
                
                writer.writerow((contract, AddressAnalyzerInBulk.create_or_update_data(methods)))

                # append as sets data structure with the idea to use set.intersection
                list_methods.append(set(methods))
        methods_intersection = set.intersection(*list_methods).difference(excluded_methods)
        return methods_intersection


    # def methods_intersection(self, addresses):
    #     # get only the smart contracts as list
    #     smart_conrtact_list = self.get_SC_and_EOAs(addresses)[0]

    #     excluded_methods = {'_fallback', 'storage', 'name'}
        
    #     list_methods = []
    #     # iterate over the SC list to decompile and capture methods
    #     for contract in smart_conrtact_list:
    #         decompile_output = self.decompile(contract)
    #         methods = AddressAnalyzerInBulk.get_methods(decompile_output)
    #         # append as sets data structure with the idea to use set.intersection
    #         list_methods.append(set(methods))

    #     result = set.intersection(*list_methods).difference(excluded_methods)
    #     return result


    def create_or_update_data(methods):
        with open('types.json', 'r') as file:
            data = file.read()

        dict_type = json.loads(data)

        result = []
        for method in methods:
            for k,v in dict_type.items():
                for value in v:
                    if value in method.lower():
                        result.append(k)

        series_mode = pd.Series(result).mode()

        return series_mode.tolist()
  
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


# Calling the get_contract_type method on the given addresses will create csv file with the respective data
print(analyzer.get_contract_type(addresses))

# Create DataFrame object from the generated csv file
df = pd.read_csv('analized.csv', names=['contract', 'probable type'])
print(df)


# "WEB3_PROVIDER_URI"  