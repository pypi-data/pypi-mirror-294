"""
Swap USDC from Arbitrum to Optimism.
"""

import pprint
import time

import requests
from web3 import Web3
from web3._utils.transactions import fill_nonce

import config


# Must have 100 units of USDC on arbitrum + gas
private_key = ""
usdc_amount = 100

# web3 for source chain
w3 = Web3(Web3.HTTPProvider(config.rpc_urls["arbitrum"]))

account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

session = requests.Session()
session.headers.update(
    {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
)

deployments = session.get(
    config.backend_url + config.endpoints["get_config"],
).json()["deployments"]

arbitrum_info = deployments["arbitrum"]
optimism_info = deployments["optimism"]

contract = w3.eth.contract(
    address=arbitrum_info["contracts"]["order_book"],
    abi=config.order_book_abi,
)

bond_fee = 0  # Percentage

place_order = contract.functions.placeOrder(
    (  # direction: OrderDirection
        arbitrum_info["assets"]["USDC"]["address"],  # srcAsset: address
        optimism_info["assets"]["USDC"]["address"],  # dstAsset: address
        optimism_info["lz_cid"],  # dstLzc: uint32
    ),
    (  # funding: OrderFunding
        usdc_amount,  # srcQuantity: uint96
        usdc_amount,  # dstQuantity: uint96
        bond_fee,  # bondFee: uint16
        optimism_info["assets"]["USDC"]["address"],  # bondAsset: address
        usdc_amount * bond_fee // 100,  # bondAmount: uint96
    ),
    (  # expiration: OrderExpiration
        int(time.time()) + 3600,  # timestamp: uint32
        0,  # challengeOffset: uint16
        0,  # challengeWindow: uint16
    ),
    False,  # isMaker: bool
)

tx_params = {
    "from": account.address,
    "value": w3.to_wei(0, "wei"),
    "nonce": w3.eth.get_transaction_count(account.address),
}
tx_params = fill_nonce(w3, tx_params)

print("Transaction parameters:")
pprint.pprint(dict(tx_params))

unsigned_tx = place_order.build_transaction(tx_params)

signed_tx = w3.eth.account.sign_transaction(unsigned_tx, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Transaction receipt:")
pprint.pprint(dict(tx_receipt))

data = {
    "chain": "arbitrum",
    "place_taker_tx": tx_hash.hex(),
}

response = session.post(
    config.backend_url + config.endpoints["orders"],
    json=data,
)

match response.status_code:
    case 200:
        print("Order success")
    case _:
        print(f"Order failure (status code {response.status_code})")

print("Response:")
pprint.pprint(response.json())
