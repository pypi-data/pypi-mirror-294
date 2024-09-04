from typing import AbstractSet, Callable

from .client import client
from .data_types import Token
from .utility import random_set_choice


# A DestinationPolicy is any function that takes the source token and produces the destination token
DestinationPolicy = Callable[[Token], Token]


def random_chain(excluded_chains: AbstractSet[str] = frozenset(("ethereum",))) -> str:
    return random_set_choice(client.chains - excluded_chains)


def random_chain_fixed_symbol_policy(symbol: str) -> DestinationPolicy:
    assert symbol != "ETH", "Cannot trade the gas token"

    def fixed_token(
        excluded_chains: AbstractSet[str] = frozenset(("ethereum",))
    ) -> Token:
        chain = random_chain(excluded_chains)
        return Token.from_components(chain, symbol)

    return lambda src_token: fixed_token(frozenset(("ethereum", src_token.chain.name)))


def random_chain_random_token_policy() -> DestinationPolicy:
    def random_token(
        excluded_chains: AbstractSet[str] = frozenset(("ethereum",)),
        excluded_symbols: AbstractSet[str] = frozenset(("ETH",)),
    ) -> Token:
        chain = random_chain(excluded_chains)
        symbol = random_set_choice(client.symbols(chain) - excluded_symbols)
        return Token.from_components(chain, symbol)

    return lambda src_token: random_token(frozenset(("ethereum", src_token.chain.name)))
