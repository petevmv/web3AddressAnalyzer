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
set up w3 provider WEB3_PROVIDER_URI=xxxxx..... to your .env file, it will load it once you run the following
```
python AddressAnalyzer.py 0x77777FeDdddFfC19Ff86DB637967013e6C6A116C
```
or address of your choise!(for this specific example is Tornado Cash)



