from thirdweb import ThirdwebSDK
import requests
from flask import Blueprint

# Talking to Moralis
def requestEVM():
    url = "https://authapi.moralis.io/challenge/request/evm"
    payload = {"timeout": 15}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "kJfYYpmMmfKhvaWMdD3f3xMMb24B4MHBDDVrfjslkKgTilvMgdwr1bwKUr8vWdHH"
    }

    response = requests.post(url, json=payload, headers=headers)

sdk = ThirdwebSDK("mumbai") # Connect to the mumbai testnet on EVM
contract = sdk.get_contract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9")
data = contract.call("claim", _receiver, _tokenId, _quantity)