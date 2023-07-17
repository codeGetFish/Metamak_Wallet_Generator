Install the required packages. To do so, run the following command:
pip install -r requirements.txt

This code can be used to generate 12 word seed phrase using Bip39 words saved in wordlist.txt for eth or solidity compatibale chains.
The quantity of wallet attempts can be changed by changing seedCounter range.
It checks to make sure the seed phrase is valid and saves the results too valid.txt
With an etherscan api key you can also check too make sure the wallet balance is zero or unused.