import random
from typing import AbstractSet

from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .client import client
from . import config
from .data_types import Token


def make_w3(token: Token) -> AsyncWeb3:
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(token.chain.rpc_url))

    if not w3.is_checksum_address(token.contract_address):
        raise ValueError("Invalid Params")

    imported_account = w3.eth.account.from_key(config.private_key)
    w3.eth.default_account = imported_account.address

    return w3


def make_token_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=AsyncWeb3.to_checksum_address(token.contract_address),
        abi=config.erc20_abi,
    )


def make_order_book_contract(w3: AsyncWeb3, token: Token) -> AsyncContract:
    return w3.eth.contract(
        address=client.deployments[token.chain.name]["contracts"]["order_book"],
        abi=config.order_book_abi,
    )


# TODO: Annotate with generics in Python 3.12+
def random_set_choice(s: AbstractSet[str]) -> str:
    return random.choice(tuple(s))
