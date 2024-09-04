import asyncio
import pprint
import time
from typing import Optional

from hexbytes import HexBytes
from web3 import AsyncWeb3
from web3.contract import AsyncContract

from .client import client
from . import config
from .data_types import Token
from .destination_policy import DestinationPolicy
from .transactions import safe_build_and_send_tx
from .utility import make_order_book_contract, make_token_contract, make_w3


BOND_FEE = 1


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

    try:
        tx_hash = await safe_build_and_send_tx(
            w3,
            config.private_key,
            public_address,
            approve_func,
        )
    except Exception as e:
        raise ValueError(f"failed to send approve tx: {e}") from e

    return tx_hash


async def test_bounce_trade(src_token: Token, destination_policy: DestinationPolicy):
    src_w3 = make_w3(src_token)
    src_contract = make_order_book_contract(src_w3, src_token)

    while True:
        dest_token = destination_policy(src_token)
        dest_w3 = make_w3(dest_token)
        dest_contract = make_order_book_contract(dest_w3, dest_token)

        print(f"Swapping {src_token} for {dest_token}")

        src_token_contract = make_token_contract(src_w3, src_token)
        src_balance: int = await src_token_contract.functions.balanceOf(
            src_w3.eth.default_account
        ).call()

        if src_balance <= 0:
            print(f"Error: source balance was empty! Cannot continue trading.")
            break

        quote = client.request_quote(
            src_token,
            dest_token,
            src_balance,
            src_w3.eth.default_account,  # type: ignore
        )

        print("Quote:")
        pprint.pprint(quote)

        if quote["invalid_amount"]:
            print("Quote had invalid amount:")
            pprint.pprint(quote)
            print("Retrying with another destination token")
            continue

        src_amount, dest_amount = quote["src_amount"], quote["dst_amount"]

        print(
            f"Can fill {src_amount=}/{src_balance=} ({100 * src_amount / src_balance}%)"
        )

        if src_amount < src_balance:
            print("Warning: not enough liquidity to trade entire source balance")

            if src_amount <= 0:
                print(f"Retrying with another destination token")
                break

        await ensure_approval(
            src_w3,
            src_w3.eth.default_account,
            src_contract.address,
            src_token.contract_address,
            src_amount,
        )

        try:
            place_order = src_contract.functions.placeOrder(
                (  # direction: OrderDirection
                    src_token.contract_address,  # srcAsset: address
                    dest_token.contract_address,  # dstAsset: address
                    dest_token.chain.lz_cid,  # dstLzc: uint32
                ),
                (  # funding: OrderFunding
                    src_amount,  # srcQuantity: uint96
                    dest_amount,  # dstQuantity: uint96
                    BOND_FEE,  # bondFee: uint16
                    dest_token.contract_address,  # bondAsset: address
                    dest_amount * BOND_FEE // 100,  # bondAmount: uint96
                ),
                (  # expiration: OrderExpiration
                    int(time.time()) + 600,  # timestamp: uint32
                    20,  # challengeOffset: uint16
                    40,  # challengeWindow: uint16
                ),
                False,  # isMaker: bool
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

            tx_receipt = await src_w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=60
            )
            print("Receipt:")
            pprint.pprint(dict(tx_receipt))

        except Exception as e:
            raise ValueError(f"Failed to send the transaction: {e}")

        try:
            order_response = client.submit_order(src_token.chain.name, tx_hash.hex())

        except Exception as e:
            print(e)
            print("\n There was an error submitting this order \n")
            await asyncio.sleep(5)
            continue

        print("Submitted order with response:")
        pprint.pprint(order_response)

        print("\n Sleeping for 120 seconds..... \n")
        await asyncio.sleep(120)

        src_token, src_w3, src_contract = dest_token, dest_w3, dest_contract
