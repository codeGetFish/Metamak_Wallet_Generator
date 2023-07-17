import random
import requests
import json
from eth_account import Account
from eth_utils.exceptions import ValidationError
import time

# Enable Mnemonic features
Account.enable_unaudited_hdwallet_features()

# Wordlist
word_list = []

# Fill wordlist from wordlist.txt
with open('wordlist.txt') as file:
    for line in file:
        word_list.append(line.strip())

# List of 0 words
zero_words = []

# Generate n number of seeds and print mnemonic addresses
for seedCounter in range(10):
    seed = zero_words.copy()

    # Append 12 words from wordlist.txt
    while len(seed) < 12:
        wordChoice = random.choice(word_list)
        if wordChoice not in seed:
            seed.append(wordChoice)

    # Add extra randomness by shuffling the order of the words
    random.shuffle(seed)

    mnemonic = " ".join(seed)
    try:
        account = Account.from_mnemonic(mnemonic)
        address = account.address

        # Check if mnemonic is already in the "valid.txt", "wallets_with_transactions.txt", "invalid.txt", "invalid2.txt", "invalid3.txt", or "invalid4.txt" files
        already_exists = False
        with open("valid.txt", "r") as validFile:
            if mnemonic in validFile.read():
                already_exists = True
        with open("wallets_with_transactions.txt", "r") as txFile:
            if mnemonic in txFile.read():
                already_exists = True

        if already_exists:
            print(f"Mnemonic already exists: {mnemonic}")
            continue

        # API request to check transaction history
        ETHAPI = "" #Place your etherscan api key here
        eth = requests.get(
            f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=99999999&page=1&offset=10&sort=asc&apikey={ETHAPI}',
            timeout=10  # Set the timeout value to 10 seconds
        )
        ethJson = eth.json()
        ethTransaction = ethJson.get("status", 0)

        if int(ethTransaction) > 0:
            print(f"Has transaction history {mnemonic} {address}")
            with open("wallets_with_transactions.txt", "a") as txFile:
                txFile.write(f"Mnemonic: {mnemonic}\nAddress: {address}\n\n")

        with open("valid.txt", "a") as validFile:
            validFile.write(f"Mnemonic: {mnemonic}\nAddress: {address}\n\n")

    except ValidationError as e:
        print(f"Invalid Mnemonic: {mnemonic}")

    print()  # Print a blank line between each seed
    time.sleep(1)  # Add a 1-second delay
