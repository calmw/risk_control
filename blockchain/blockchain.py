import logging

from web3 import Web3

from abi.abi import getABI


# 获取代币余额
def getERC20TokenBalance(rpc, contractAddress, address):
    try:
        address = Web3.to_checksum_address(address)
        abi = getABI("ERC20")
        w3 = Web3(Web3.HTTPProvider(rpc))
        contract = w3.eth.contract(address=contractAddress, abi=abi)
        return contract.functions.balanceOf(address).call()
    except Exception as e:
        print(e)
        logging.error("getERC20TokenBalance error:", e)
        return None


# 获取原生币余额
def getNativeCoinBalance(rpc, address):
    try:
        address = Web3.to_checksum_address(address)
        w3 = Web3(Web3.HTTPProvider(rpc))
        return w3.eth.get_balance(address) / 1000000000000000000
    except Exception as e:
        logging.error("getNativeCoinBalance error:", e)
        return None
