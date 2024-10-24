from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy



FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development","ganache-local"]
DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_LOCAL_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def get_gas_price():
        if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            return 0
        else:
            gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
            gas_price(gas_strategy)
        return gas_strategy

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator)<=0:
        MockV3Aggregator.deploy(DECIMALS,STARTING_PRICE,{"from": get_account()})
    print("Mocks deployed!")