import argparse
import asyncio
import json
import pathlib
import pprint
import typing

import eth_account
from eth_account.signers.local import LocalAccount

from .client import client
from .data_types import Token
from .destination_policy import (
    random_chain_fixed_symbol_policy,
    random_chain_random_token_policy,
)
from .run_script import initialize_config, test_bounce_trade
from .withdraw import drain_all

USAGE = """
cctt generate --password PASSWORD
    Generate a random ETH public-private key-pair. Outputs the public key and writes the encrypted account to the account file.
    Warning: overwrites existing account file. This is irreversible.

cctt import --password PASSWORD --private-key PRIVATE_KEY
    Import an existing account corresponding to the given private key. Outputs the public key and writes the encrypted account to the account file.
    Warning: overwrites existing account file. This is irreversible.

cctt decrypt --password PASSWORD
    Display the public-private key pair in the account file, decrypted with the password.

cctt balances
    Display balances of all tokens on all supported chains.

cctt run --password PASSWORD --source arbitrum-USDC --destination USDC
    Perform the test using the account in the account file. 
    The first trade is made from the chain and symbol specified by the --source argument.
    In each trade, a random chain is chosen as the destination chain and the entire balance of the source token is sold for the destination token.
    The choice of destination token is controlled by the --destination argument.
    In the next trade, the destination token becomes the new source token.
    This repeats until the program is stopped.

    Note: currently does not support trading the gas token (ETH) on any chain.

cctt withdraw --password PASSWORD -wallet WALLET
    Withdraw all tokens and gas (ETH) on all supported chains from the account into the provided wallet address.
"""

DESCRIPTION = "Cross chain trade test (CCTT) - test swaps between random chains"

DEFAULT_ACCOUNT_FILEPATH = pathlib.Path("account.json")

DEFAULT_SOURCE_TOKEN = Token("arbitrum-USDC")

DEFAULT_DESTINATION_POLICY = "USDC"

DESTINATION_POLICY_DESCRIPTION = f"""
Controls how the destination token is chosen in each trade.
If set to 0, a randomly chosen destination token will be used in each trade.
If set to a string SYMBOL, then chain-SYMBOL will be used as the destination token, where chain is randomly chosen.
Defaults to {DEFAULT_DESTINATION_POLICY}.
"""


# Returns the account object
def read_account(password: str, account_filepath: pathlib.Path) -> LocalAccount:
    with open(account_filepath, "r") as account_file:
        encrypted = json.load(account_file)

    decrypted = eth_account.Account.decrypt(encrypted, password)
    account = eth_account.Account.from_key(decrypted)

    return account


# Writes an encrypted account
def write_account(encrypted: dict, account_filepath: pathlib.Path) -> None:
    with open(account_filepath, "w") as account_file:
        account_file.write(json.dumps(encrypted))


async def run() -> None:

    parser = argparse.ArgumentParser(
        prog="cctt",
        usage=USAGE,
        description=DESCRIPTION,
    )

    parser.add_argument(
        "command",
        choices=("generate", "import", "decrypt", "balances", "run", "withdraw"),
        help="Command to perform",
        nargs="?",
        type=str,
    )

    parser.add_argument(
        "--private-key",
        "-k",
        dest="private_key",
        help="Hex private key of the account you'd like to import",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--password",
        "-p",
        dest="password",
        help="Password used to encrypt/decrypt the private key",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--wallet",
        "-w",
        dest="wallet",
        help="Hex destination wallet address for withdrawal",
        nargs="?",
        required=False,
        type=str,
    )

    parser.add_argument(
        "--file",
        "-f",
        default=DEFAULT_ACCOUNT_FILEPATH,
        dest="account_filepath",
        help=f"Path to the JSON file storing the encrypted account data, defaulting to {DEFAULT_ACCOUNT_FILEPATH}",
        required=False,
        nargs="?",
        type=pathlib.Path,
    )

    parser.add_argument(
        "--source",
        "-s",
        default=DEFAULT_SOURCE_TOKEN,
        dest="src_token",
        help=f"The initial token to be sold in the first trade in the form of chain-SYMBOL, defaulting to {DEFAULT_SOURCE_TOKEN}",
        required=False,
        nargs="?",
        type=Token,
    )

    parser.add_argument(
        "--destination",
        "-d",
        default=DEFAULT_DESTINATION_POLICY,
        dest="destination_policy",
        help=DESTINATION_POLICY_DESCRIPTION,
        required=False,
        nargs="?",
        type=str,
    )

    arguments = parser.parse_args()

    command: str = arguments.command
    account_filepath: pathlib.Path = arguments.account_filepath
    assert account_filepath, "Account filepath required"

    if command == "balances":
        with open(account_filepath, "r") as account_file:
            encrypted = json.load(account_file)

        wallet = f"0x{encrypted['address']}"

        print("Balances:")
        pprint.pprint(client.get_token_balances(wallet))

        return

    password: str = arguments.password
    src_token: Token = arguments.src_token

    assert command, "Command required"
    assert password, "Password required"
    assert src_token.symbol != "ETH", "Cannot trade the gas token"

    match command:
        case "generate":
            account = eth_account.Account.create()

        case "import":
            private_key = arguments.private_key
            assert private_key, "Private key must be provided to import wallet"
            account = eth_account.Account.from_key(private_key)

        case _:
            account = read_account(password, account_filepath)

    public_key, private_key = account.address, account.key

    print(f"Public key: {public_key}")

    match command:
        case "generate" | "import":
            encrypted = eth_account.Account.encrypt(private_key, password)
            write_account(encrypted, account_filepath)

        case "decrypt":
            print(f"Private key: {private_key.hex()}")

        case "run":
            initialize_config(private_key)

            destination_policy_str = arguments.destination_policy

            match destination_policy_str:
                case "0":
                    print("Destination token policy: randomize")
                    destination_policy = random_chain_random_token_policy()

                case _ as symbol:
                    print(f"Destination token policy: fixed symbol {symbol}")
                    destination_policy = random_chain_fixed_symbol_policy(symbol)

            await test_bounce_trade(src_token, destination_policy)

        case "withdraw":
            initialize_config(private_key)

            wallet = arguments.wallet
            assert wallet, "Destination wallet must be provided for withdrawal"

            await drain_all(public_key, private_key, wallet)

        case _ as unreachable:
            typing.assert_never(unreachable)  # type: ignore


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
