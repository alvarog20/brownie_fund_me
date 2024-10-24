from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (get_account, get_gas_price, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS)
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

# gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)

# gas_price(gas_strategy)
import time
from web3 import Web3



def deploy_fund_me():
    account = get_account()
    #if we are on a persistent network like sepolia, use the associated address
    #otherwise, deploy mocks
    gas_strategy=get_gas_price()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address =config["networks"][network.show_active()]["eth_usd_price_feed"]
        fund_me = FundMe.deploy(price_feed_address,{"from": account,"gas_price": gas_strategy},publish_source=config["networks"][network.show_active()].get("verify"))
        time.sleep(1)
    else:
        deploy_mocks()
        price_feed_address=MockV3Aggregator[-1].address
        fund_me = FundMe.deploy(price_feed_address,{"from": account},publish_source=config["networks"][network.show_active()].get("verify"))
        time.sleep(1)
        

    # fund_me = FundMe.deploy(price_feed_address,{"from": account, "gas_price": gas_strategy},publish_source=config["networks"][network.show_active()].get("verify"))

    print(f"Contract deployed to {fund_me.address}")
    return fund_me



def main():
    deploy_fund_me()


