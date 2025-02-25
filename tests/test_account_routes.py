import pytest
from app.models import Account
from app import db

def test_get_balance(client, sample_account):
    """
    Test retrieving an account balance.
    """
    response = client.get(f"/accounts/{sample_account.account_number}/balance")
    json_data = response.get_json()

    assert response.status_code == 200
    assert "balance" in json_data["data"]
    assert json_data["data"]["account_number"] == sample_account.account_number

def test_withdraw(client, sample_account):
    """
    Test withdrawing money from an account.
    """
    response = client.post(f"/accounts/{sample_account.account_number}/withdraw", json={"amount": 100})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["data"]["new_balance"] == 400.0  # 500 - 100

def test_deposit(client, sample_account):
    """
    Test depositing money into an account.
    """
    response = client.post(f"/accounts/{sample_account.account_number}/deposit", json={"amount": 200})
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["data"]["new_balance"] == 700.0  # 500 + 200
