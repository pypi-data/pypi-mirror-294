import asyncio
from collections import defaultdict
import pprint
import time
from typing import Optional

from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .balances import get_balance, get_gas_balance
from .client import client
from . import config
from .data_types import Token
from .destination_policy import DestinationPolicy, TriedTokenDict
from .transactions import safe_build_and_send_tx
from .utility import (
    make_order_book_contract,
    make_token_contract,
    make_w3_from_token,
)


def initialize_config(private_key: HexBytes) -> None:
    assert "production" in config.backend_url, "Backend URL should point to production"
    config.private_key = private_key.hex().removeprefix("0x")


async def ensure_approval(
    w3: AsyncWeb3, public_address, spender_address, src_address, amount: int
) -> Optional[HexBytes]:
    contract: AsyncContract = w3.eth.contract(address=src_address, abi=config.erc20_abi)

    try:
        allowance_func = contract.functions.allowance(
            public_address,
            spender_address,
        )
    except Exception as e:
        raise ValueError(f"failed to build allowance function: {e}") from e

    try:
        allowance: int = await allowance_func.call()
    except Exception as e:
        raise ConnectionError(f"failed to get allowance: {e}") from e

    print(f"Allowance of {allowance=}/{amount=} ({100 * allowance / amount}%)")

    if allowance >= amount:
        return None

    try:
        approve_func = contract.functions.approve(
            spender_address,
            amount,
        )
    except Exception as e:
        raise ValueError(f"failed to build approve function: {e}") from e

    print("Approving larger allowance")
    try:
        tx_hash = await safe_build_and_send_tx(
            w3,
            config.private_key,
            public_address,
            approve_func,
        )
    except Exception as e:
        raise ValueError(f"failed to send approve tx: {e}") from e

    print(f"Approval transaction hash: {tx_hash.hex()}")
    return tx_hash


async def test_bounce_trade(src_token: Token, destination_policy: DestinationPolicy):
    src_w3 = make_w3_from_token(src_token)
    src_order_book_contract = make_order_book_contract(src_w3, src_token)

    excluded_chains = set(config.excluded_chains)

    tried_tokens: TriedTokenDict = defaultdict(set)
    tried_tokens[src_token.chain.name].add(src_token.symbol)

    while True:
        print()
        
        src_balance = await get_balance(src_w3, src_token)

        if src_balance <= 0:
            print(f"Error: source balance was empty! Cannot continue trading.")
            break

        dest_token = destination_policy(tried_tokens, excluded_chains)
        tried_tokens[dest_token.chain.name].add(dest_token.symbol)
        dest_w3 = make_w3_from_token(dest_token)

        print(f"Swapping {src_token} for {dest_token}")

        if await get_gas_balance(dest_w3) <= 0:
            print(
                f"No gas on chain {dest_token.chain.name}, will be excluded from future selection"
            )
            excluded_chains.add(dest_token.chain.name)
            print("Trying another destination")
            continue

        quote = client.request_quote(
            src_token,
            dest_token,
            src_balance,
            src_w3.eth.default_account,  # type: ignore
        )

        print("Quote:")
        pprint.pprint(quote)

        assert (
            quote["src_asset_address"] == src_token.contract_address
        ), f"Need {quote['src_asset_address']=} to equal {src_token.contract_address=}"

        if quote["invalid_amount"]:
            print("Quote had invalid amount:")
            pprint.pprint(quote)
            print("Trying another destination")
            continue

        src_amount, dest_amount = quote["src_amount"], quote["dst_amount"]

        print(
            f"Can fill {src_amount=}/{src_balance=} ({100 * src_amount / src_balance}%)"
        )

        assert src_amount <= src_balance

        if src_amount < src_balance:
            print("Warning: not enough liquidity to trade entire source balance")

            if src_amount <= 0:
                print(f"Trying another destination")
                break

        try:
            await ensure_approval(
                src_w3,
                src_w3.eth.default_account,
                src_order_book_contract.address,
                src_token.contract_address,
                src_amount,
            )
        except Exception as e:
            print(f"Failed to ensure approval: {e}")
            continue

        try:
            order_direction = (
                src_token.contract_address,  # srcAsset: address
                dest_token.contract_address,  # dstAsset: address
                dest_token.chain.lz_cid,  # dstLzc: uint32
            )

            order_funding = (
                src_amount,  # srcQuantity: uint96
                dest_amount,  # dstQuantity: uint96
                quote["bond_fee"],  # bondFee: uint16
                quote["bond_asset_address"],  # bondAsset: address
                quote["bond_amount"],  # bondAmount: uint96
            )

            order_expiration = (
                int(time.time()) + 3600,  # timestamp: uint32
                quote["challenge_offset"],  # challengeOffset: uint16
                quote["challenge_window"],  # challengeWindow: uint16
            )

            is_maker = False

            place_order = src_order_book_contract.functions.placeOrder(
                order_direction,
                order_funding,
                order_expiration,
                is_maker,
            )

            gas_estimate = await place_order.estimate_gas(
                {
                    "from": src_w3.eth.default_account,  # type: ignore
                    "value": src_w3.to_wei(0, "wei"),
                }
            )
            gas_price = await src_w3.eth.gas_price
            print(
                f"estimated gas approve chain {src_token.chain.name} {gas_estimate} and gas_price {gas_price}"
            )

            tx_hash = await safe_build_and_send_tx(
                src_w3,
                config.private_key,
                src_w3.eth.default_account,  # type: ignore
                place_order,
            )
            print(f"Placed order with hash: {tx_hash.hex()}")

            tx_receipt = await src_w3.eth.wait_for_transaction_receipt(tx_hash)
            print("Receipt:")
            pprint.pprint(dict(tx_receipt))

        except Exception as e:
            print(f"Failed to send the transaction: {e}")
            continue

        try:
            order_response = client.submit_order(src_token.chain.name, tx_hash.hex())

        except Exception as e:
            print(e)
            print("There was an error submitting this order")
            await asyncio.sleep(5)
            continue

        print("Submitted order with response:")
        pprint.pprint(order_response)

        print(f"Sleeping for {config.timeout} seconds")
        await asyncio.sleep(config.timeout)

        if (balance := await get_balance(dest_w3, dest_token)) < dest_amount:
            print(f"Warning: {balance} received from trade less than {dest_amount} expected, transaction may not have completed within timeout period")

            if balance <= 0:
                raise RuntimeError(f"Balance not received on destination chain within timeout")

        src_token, src_w3, src_order_book_contract = (
            dest_token,
            dest_w3,
            make_order_book_contract(dest_w3, dest_token),
        )

        tried_tokens.clear()
        tried_tokens[src_token.chain.name].add(src_token.symbol)
