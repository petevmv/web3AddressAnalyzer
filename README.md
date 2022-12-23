# web3AddressAnalyzer

## Simple address analyzer for probable smart contract types.
It's not refined, a lot more has to be done to be there!
Can decompile all of ETH mainnet.
Makes RESTful API get request to https://www.4byte.directory/ **with the verify flag set to False**, otherwise get request fails.

## Heavy lifting is done by panoramix-decompiler(https://github.com/palkeo/panoramix), some smart contract can take several minutes to decompile, don't interpupt it as it may end up with the annoying Traceback database disk image malformed.(Strongly suggesting using virtualenv for best practices)


### Installation:
```
git clone https://github.com/petevmv/web3AddressAnalyzer.git
pip install -r requirements.txt
```


### Running:
set up w3 provider WEB3_PROVIDER_URI=xxxxx..... to your .env file, it will load it once you run either of the following 
```
python AddressAnalyzer.py 0x77777FeDdddFfC19Ff86DB637967013e6C6A116C
```
for one address at a time or address of your choise!(for this specific example is Tornado Cash)

<b>or<b>


for multyple addresses paste the contracts you want as a list into the file to_analize.txt and run:

```
python AddressAnalyzerInBulk.py

```
Final result is a .csv file that is passed to the pandas DataFrame and displayed. Every run the csv file is modifed and updated with the old and new data or if there is no such file - it will be created while running. 


 



