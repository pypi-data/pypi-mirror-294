from collections import defaultdict
from typing import AbstractSet, Callable

from .client import client
from .data_types import Token
from .utility import random_set_choice


# Maps chains to symbols that have already been tried on that chain
# Default factory: set
TriedTokenDict = defaultdict[str, set[str]]

# Takes a dictionary mapping chains to symbols that have already been tried, and a set of excluded chains. Produces a viable destination token for the next trade.
DestinationPolicy = Callable[[TriedTokenDict, set[str]], Token]


def random_chain(excluded_chains: AbstractSet[str]) -> str:
    return random_set_choice(client.chains - excluded_chains)


def random_chain_fixed_symbol_policy(symbol: str) -> DestinationPolicy:
    def fixed_token(
        tried_tokens: TriedTokenDict,
        excluded_chains: set[str],
    ) -> Token:
        try:
            chain = random_chain(excluded_chains | frozenset(tried_tokens.keys()))

            if client.gas_tokens.get(chain) == symbol:
                raise RuntimeError(f"Cannot trade the gas token {chain}-{symbol}")

            if symbol not in client.symbols(chain):
                print(f"Chose chain {chain} but it did not have the fixed symbol {symbol} required by the policy")
                print(f"Excluding {chain} from further selection")
                excluded_chains.add(chain)
                print("Retrying")
                return fixed_token(tried_tokens, excluded_chains)

            return Token.from_components(chain, symbol)
        except IndexError:
            print(f"{tried_tokens=}")
            print(f"{excluded_chains=}")
            raise RuntimeError("Unable to choose destination token - all possibilities have been excluded")

    return lambda tried_tokens, excluded_chains: fixed_token(
        tried_tokens, excluded_chains
    )


def random_chain_random_token_policy() -> DestinationPolicy:
    def random_token(tried_tokens: TriedTokenDict, excluded_chains: set[str]) -> Token:
        try:
            chain = random_chain(excluded_chains | frozenset(tried_tokens.keys()))

            tried_symbols = tried_tokens[chain]
            gas_token = client.gas_tokens.get(chain)
            excluded_symbols = (
                tried_symbols if not gas_token else tried_symbols | frozenset((gas_token,))
            )

            symbol = random_set_choice(client.symbols(chain) - excluded_symbols)

            return Token.from_components(chain, symbol)
        except IndexError:
            print(f"{tried_tokens=}")
            print(f"{excluded_chains=}")
            raise RuntimeError("Unable to choose destination token - all possibilities have been excluded")

    return lambda tried_tokens, excluded_chains: random_token(
        tried_tokens, excluded_chains
    )
