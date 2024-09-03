from typing import Tuple

from web3 import Web3
from eth_utils.abi import function_abi_to_4byte_selector, collapse_if_tuple

from action_set_lib.utils.contact_tool import get_contact_address

token_mapping = {
  "USDC": "0xBfcB0b8956cE46e561C05f3cd75B1370311B7DAa",
  "USDT": "0xBfcB0b8956cE46e561C05f3cd75B1370311B7DAa",
  "wETH": "0xBfcB0b8956cE46e561C05f3cd75B1370311B7DAa"
}

usdc_abi = [
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "from",
        "type": "address"
      },
      {
        "internalType": "address",
        "name": "to",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "controlTransferFrom",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "owner_",
        "type": "address"
      }
    ],
    "name": "setOwner",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      }
    ],
    "name": "setToken",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "token_",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "value",
        "type": "uint256"
      }
    ],
    "name": "withdraw",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "stateMutability": "payable",
    "type": "receive"
  },
  {
    "inputs": [],
    "name": "TRANSFER",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "TRANSFERFROM",
    "outputs": [
      {
        "internalType": "bytes4",
        "name": "",
        "type": "bytes4"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]

def transfer_auto(receiver, amount, chain = "Base", token = "0xBfcB0b8956cE46e561C05f3cd75B1370311B7DAa", **kwargs):
    """
      kwargs need to include providers from different chains
      for example: providers: {
                                "Base": "https://base.g.alchemy.com/v2/7mj7kTlPr2M1AiMu42Z3Tbwwg8DyOHPk", 
                                "Ethereum": "https://ethereum.g.alchemy.com/v2/7mj7kTlPr2M1AiMu42Z3Tbwwg8DyOHPk" 
                              }
    """
    info = None
    executor = kwargs.get("executor")
    redis_client = kwargs.get("redis_client")
    control_address = kwargs.get('control_address')
    control_contract = kwargs.get('contract')
    private_key = kwargs.get('private_key')
    blockchain_explore = kwargs.get('blockchain_explore')
    providers = kwargs.get("providers")
    provider = Web3.HTTPProvider(providers[chain])
    provider.middlewares.clear()
    w3 = Web3(provider)
    code, res = get_contact_address(redis_client, executor, receiver, w3)
    if code != 200:
        info = {"content": f"Cannot find {name} on contact", "code": 420}
        return info;
    value = float(amount)
    amount_to_transfer = w3.to_wei(value, 'mwei')  # USDT uses 6 decimals
    receiver = res
    to = w3.to_checksum_address(receiver)
    executor = w3.to_checksum_address(executor)

    print(f"to: {to}, executor: {executor}")
    tx_hash = None
    try:
        nonce = w3.eth.get_transaction_count(control_address)
        current_gas_price = w3.eth.gas_price
        replacement_gas_price = current_gas_price
        tx = control_contract.functions.transferFromERC20(
            token, executor, to, amount_to_transfer).build_transaction({
                'from':
                control_address,
                'nonce':
                nonce,
                'gas':
                200000,  # Adjust gas limit
                'gasPrice':
                replacement_gas_price,  # Adjust gas price
            })
        pk = private_key
        signed_tx = w3.eth.account.sign_transaction(tx, pk)
        send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = send_tx.hex()
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        status = 200
        message = "success"
        if tx_receipt['status'] == 0:
            status = 500
            message = "failed"
        info = {
            "content":
            generate_markdown_content(tx_receipt['status'], tx_hash, blockchain_explore),
            "status":
            tx_receipt['status'],
            "code":
            status
        }
        return info
    except Exception as e:
        name, params = decode_custom_error(usdc_abi, w3, str(e))
        if not name:
            # Note: If unknown error expose, check:
            # 1. if abi.json is the latest
            # 2. what error is exposed, how it happens
            message = f"Transfer usdt failed with unknown error: {e}"
        else:
            message = f"Transfer usdt error, error name: {name}, parameters: {params}"
        info = {"content": message, "status": 0, "code": 500}
        return info

def generate_markdown_content(status, hash_value, blockchain_explore):
    if status == 1:
        return f"Transfer successful. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"
    else:
        return f"Transfer failed. You can check the transaction on [blockchain explorer]({blockchain_explore}{hash_value})"

def decode_custom_error(contract_abi, w3, error) -> Tuple[str, str]:
    # Parse error content, the error content must look like:
    # "Call method: submitServiceProof,xxxxx,error:('xxxxxx','xxxxxxx')"
    tmp_array = error.split(":")
    if len(tmp_array) != 3:
        return None, None
    param_str = tmp_array[2]
    param_str = param_str.replace("(","")
    param_str = param_str.replace(")","")
    param_str = param_str.replace(",","")
    param_str = param_str.replace("'","")
    errors = param_str.split()

    for error in [abi for abi in contract_abi if abi["type"] == "error"]:
        # Get error signature components
        name = error["name"]
        data_types = [collapse_if_tuple(abi_input) for abi_input in error.get("inputs", [])]
        error_signature_hex = function_abi_to_4byte_selector(error).hex()
        # Find match signature from error
        for error in errors:
            if error_signature_hex.casefold() == error[2:10].casefold():
                params = ','.join([str(x) for x in w3.codec.decode(data_types,bytes.fromhex(error[10:]))])
                #decoded = "%s(%s)" % (name , str(params))
                return name, params
    return None, None #try other contracts until result is not None since error may be raised from another called contract
