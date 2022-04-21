from brownie import network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.deploy import deploy_token_farm_and_happy_token
import pytest


def test_stake_and_issue_correct_amounts(amount_staked):
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing!")
    token_farm, happy_token = deploy_token_farm_and_happy_token()
    account = get_account()
    happy_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, happy_token.address, {"from": account})
    starting_balance = happy_token.balanceOf(account.address)
    price_feed_contract = get_contract("dai_usd_price_feed")
    (_, price, _, _, _) = price_feed_contract.latestRoundData()

    amount_token_to_issue = (
        price / 10 ** price_feed_contract.decimals()
    ) * amount_staked
    # Act
    dis_tx = token_farm.distribute(account.address, {"from": account})
    dis_tx.wait(1)
    issue_tx = token_farm.getRewardTokens(happy_token, {"from": account})
    issue_tx.wait(1)
    # Assert
    assert (
        happy_token.balanceOf(account.address)
        == amount_token_to_issue + starting_balance
    )
