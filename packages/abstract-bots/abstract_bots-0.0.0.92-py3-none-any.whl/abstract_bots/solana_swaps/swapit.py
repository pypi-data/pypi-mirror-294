import time, requests, json, struct, os, base58, sys, base64
from solana.transaction import AccountMeta, Transaction
from spl.token.instructions import create_associated_token_account, get_associated_token_address
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solana.rpc.types import TokenAccountOpts, TxOpts
from typing import Optional, Union
from solders.keypair import Keypair
from solders.hash import Hash
from solana.rpc.api import Client
from construct import Padding, Struct, Int64ul, Flag
from abstract_utilities import get_any_value
from abstract_security import get_env_value
from pumpFunKeys import get_pump_fun_data
from utils import *
from pumpFunKeys import get_pump_fun_data
def get_coin_data(mint_str):
    return get_pump_fun_data(str(mint_str))
def isListZero(obj):
    if obj and isinstance(obj, list):
        return obj[0]
    return obj

def get_account_by_owner(payer, mint_str: str) -> dict:
    result = asyncio.run(asyncPostRequest(url=getEndpointUrl("getTokenAccountsByOwner"), data={"account":payer,"mint":mint,"encoding":"jsonParsed"}))
    if not result or 'value' not in result:
        return None

    accounts = result.get('value', [])
    if accounts:
        return accounts[0]  # Return the first account found
    return None

def check_existing_token_account(owner: Pubkey, mint: Pubkey):
    try:
        account_data = get_account_by_owner(str(owner), str(mint))
        if account_data:
            token_account = account_data['pubkey']
            print(f"Existing token account found: {token_account}")
            return token_account, None
        else:
            print("No existing token account found. Creating a new one...")
            token_account = get_associated_token_address(owner, mint)
            token_account_instructions = create_associated_token_account(owner, owner, mint)
            return token_account, token_account_instructions
    except Exception as e:
        print(f"Error checking or creating token account: {e}")
        return None, None

def pump_fun_buy(mint_str: str, sol_in: float = 0.001, slippage: int = 25) -> bool:
    coin_data = get_coin_data(mint_str)
    print("Coin Data:", coin_data)

    if not coin_data:
        print("Failed to retrieve coin data...")
        return False

    payer_keypair = Keypair.from_base58_string(get_env_value(key='AMM_P'))
    owner = payer_keypair.pubkey()
    print("Owner Public Key:", owner)

    mint = Pubkey.from_string(mint_str)
    token_account, token_account_instructions = check_existing_token_account(owner, mint)
    print("Token Account:", token_account)

    if not token_account:
        print("Failed to retrieve or create token account.")
        return False

    virtual_sol_reserves = coin_data['virtual_sol_reserves']
    virtual_token_reserves = coin_data['virtual_token_reserves']
    sol_in_lamports = sol_in * LAMPORTS_PER_SOL
    amount = int(sol_in_lamports * virtual_token_reserves / virtual_sol_reserves)
    print("Calculated Amount:", amount)

    buildTxn(mint, amount, slippage, token_account, sol_in, token_account_instructions, buy=True)

    time.sleep(2)

    return True

mint_str = "8GKpBuFS37H1dCM4m716PJ5mjgYSePuXZMikmfvHpump"
pump_fun_buy(mint_str=mint_str, sol_in=0.0015, slippage=25)
