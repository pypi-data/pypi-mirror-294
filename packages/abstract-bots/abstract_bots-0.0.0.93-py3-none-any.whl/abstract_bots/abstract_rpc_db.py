from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import sessionmaker,declarative_base
from datetime import datetime
from abstract_security import *
from abstract_apis import postRequest
from abstract_solcatcher import view_table
import requests,os,json
Base = declarative_base()
def make_lower(string):
    newString=''
    for i,char in enumerate(string):
        if char in list('abcdefghijklmnopqrstuvwxyz'.upper()):
            char = f"_{char.lower()}"
        newString+=char
    return newString.strip('_')
def get_env_key(dbType,typ):
    input(get_env_value(f"{dbType}_{typ}"))
    return get_env_value(f"{dbType}_{typ}")
# Load environment variables
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def get_unique(method):
    return {
        "get_account_info": {"unique": "address", "getNew": True},
        "get_token_account_balance": {"unique": "address", "getNew": True},
        "get_token_accounts_by_delegate": {"unique": "address", "getNew": True},
        "get_token_accounts_by_owner": {"unique": "address", "getNew": True},
        "get_all_signatures": {"unique": "address", "getNew": True},
        "get_token_supply": {"unique": "address", "getNew": False},
        "get_block_time_from_slot": {"unique": "slot", "getNew": False},
        "get_signature_for_address": {"unique": "signature", "getNew": True},
        "fetch_account_data": {"unique": "address", "getNew": False},
        "get_transaction": {"unique": "signature", "getNew": False}
    }.get(make_lower(method))

class dbConfig(metaclass=SingletonMeta):
    def __init__(self, dbUrl=None, dbType='SOLCATCHER'):
        self.dbUrl = dbUrl or f"postgresql://{get_env_key(dbType,'USER')}:{get_env_key(dbType,'PASSWORD')}@{get_env_key(dbType,'HOST')}:{get_env_key(dbType,'PORT')}/{get_env_key(dbType,'DBNAME')}"
        self.engine = create_engine(self.dbUrl)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

def create_response_data_class(tablename, call_type, unique_column):
    # Create a dictionary with the column definitions
    columns = {
        'id': Column(Integer, primary_key=True, autoincrement=True),
        unique_column: Column(String, nullable=False),  # Unique column
        'response': Column(Text, nullable=False)
    }

    # Dynamically create the class with the correct table name and columns
    ResponseData = type(
        'ResponseData',
        (Base,),
        {
            '__tablename__': tablename,
            **columns
        }
    )

    return ResponseData

def save_response_data(signature, call_type, response):
    session = dbConfig().session
    response_json = json.dumps(response)
    unique_column = get_unique(call_type).get("unique")
    tablename = make_lower(call_type)
    
    # Dynamically create the ResponseData class with the correct table name
    ResponseDataClass = create_response_data_class(tablename, call_type, unique_column)
    
    # Add the new record
    response_data = ResponseDataClass(
        **{unique_column: signature, 'response': response_json}
    )
    
    session.add(response_data)
    try:
        session.commit()
        print("Response data saved successfully.")
    except Exception as e:
        print("Error saving response data:", e)
        session.rollback()

# Example preSave_response function
def preSave_response(call_type, params, response, signature=None):
    data = {"call_type": call_type, "params": params, "response": response}
    signature = params[0] if isinstance(params[0], str) else None
    save_response_data(signature, call_type, data)

# Example fetch_response_data function
def fetch_response_data(unique_column, signature, call_type):
    existing_entry = view_table(table_name=make_lower(call_type), column_name=make_lower(unique_column), search_string=signature)
    input(existing_entry)
    if existing_entry and existing_entry.get('error')==None:
        print(f"Found existing entry for {unique_column}: {signature} and call type: {call_type}.")
        return existing_entry
    return None

def get_solana_rpc(rpc=None):
    rpc = rpc or 'mainnet'
    for each in ['mainnet-beta','devnet','testnet']:
        if rpc in each:
            rpc=f'https://api.{each}.solana.com'
            break
    return rpc
class rpcCallDbManager(metaclass=SingletonMeta):
    def __init__(self,rpc=None, dbUrl=None, dbMgr=None):
        if not hasattr(self, 'initialized'):  # Prevent reinitialization
            self.dbUrl=dbUrl
            self.dbMgr = dbMgr or dbConfig(self.dbUrl)
            self.initialized = True
            self.rpc=get_solana_rpc(rpc=rpc)
            self.recently_checked_signature_data = {}

    def get_result(self, response):
        try:
            response = response.json()
        except:
            return response.text
        if isinstance(response, dict) and 'result' in response:
            return response['result']
        return response

    def get_conditions(self, conditions):
        return {k: v for k, v in conditions.items() if v is not None}

    def get_response(self, method, params):
        signature = params[0] if isinstance(params[0], str) else None
        unique_actions = get_unique(method)
        if unique_actions.get("getNew") == False:
            existing_response = fetch_response_data(unique_actions.get("unique"),signature, call_type)
            if existing_response:
                return existing_response

        response = self.rpc_call(call_type, params)
        if isinstance(response, dict) and response.get('error') is not None:
            return response

        preSave_response(call_type,params,response)
        return response

    def rpc_call(self, method, params):
        rpc_url = self.rpc
        # Replace with your actual RPC URL
        headers = {"Content-Type": "application/json"}
        request_data = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }
        return postRequest(rpc_url,request_data, headers)

    def get_transaction(self,signature):
        return self.get_response("getTransaction", [signature, {"maxSupportedTransactionVersion": 0}])

    def fetch_account_data(self, account):
        return self.json_rpc_call("AddressLookupTableAccount", [account, {"maxSupportedTransactionVersion": 0}])

    def get_signature_for_address(self, account=None, address=None, limit=10, until=None, after=None, finalized=True):
        account = account or address
        conditions = self.get_conditions({
            "limit": limit,
            "until": until,
            "after": after,
            "finalized": finalized,
        })
        return self.json_rpc_call("getSignaturesForAddress", [account, conditions])
    def get_account_info(self, account=None, address=None, encoding='jsonParsed'):
        account = account or address
        conditions = self.get_conditions({"encoding": encoding})
        return self.json_rpc_call("getAccountInfo", [account, conditions])

    def get_token_account_balance(self, account=None, address=None, mint=None):
        account = account or address
        conditions = self.get_conditions({"mint": mint, "commitment": 0})
        return self.json_rpc_call("getTokenAccountBalance", [account, conditions])

    def get_token_accounts_by_delegate(self, account=None, address=None, programId=None, encoding='jsonParsed'):
        account = account or address
        conditions = self.get_conditions({"programId": programId, "encoding": encoding})
        return self.json_rpc_call("getTokenAccountsByDelegate", [account, conditions])

    def get_token_accounts_by_owner(self, account=None, address=None, mint=None, encoding='jsonParsed'):
        account = account or address
        conditions = self.get_conditions({"mint": mint, "encoding": encoding})
        return self.json_rpc_call("getTokenAccountsByOwner", [account, conditions])

    def get_all_signatures(self, address, before=None, after=None, blockTime=None, slot=None, get_any=False, limit=1000):
        n_sig = 0 if after else -1
        direction = [after, before]
        last_signature = direction[n_sig]
        all_valid_signatures = []
        while True:
            signatures = self.get_signature_for_address(address, limit=limit, before=direction[0], after=direction[-1])
            if get_any or not is_full_call(signatures, limit) or is_last_signature_the_comp(signatures, direction[n_sig]) or check_before_and_after(signatures, blockTime=blockTime, slot=slot):
                if (is_last_signature_the_comp(signatures, direction[n_sig]) or check_before_and_after(signatures, blockTime=blockTime, slot=slot)) or not is_full_call(signatures, limit):
                    all_valid_signatures = combine_signatures(all_valid_signatures, signatures, n_sig)
                if all_valid_signatures or not is_full_call(signatures, limit):
                    return all_valid_signatures
            all_valid_signatures = combine_signatures(all_valid_signatures, signatures, n_sig)
            direction[n_sig] = signatures[n_sig]['signature']

    def get_token_supply(self, token):
        return self.json_rpc_call("getTokenSupply", [token])

    def get_block_time_from_slot(self, slot):
        return self.json_rpc_call("getBlockTime", [int(slot)])

    def json_rpc_call(self, call_type, params):
        signature = params[0] if isinstance(params[0], str) else None
        existing_response = fetch_response_data(get_unique(call_type).get('unique'),signature, call_type)
        if existing_response:
            return existing_response

        response = self.rpc_call(call_type, params)
        if isinstance(response, dict) and response.get('error') is not None:
            return response

        preSave_response(call_type,params,response,signature)
        return response

