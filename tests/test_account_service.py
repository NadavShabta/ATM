import pytest
from app.services.account_service import get_balance_service, withdraw_service, deposit_service

def test_get_balance_service(db_session, sample_account):
    result = get_balance_service("123456")
    assert result["success"] is True
    assert result["balance"] == 500.0

def test_withdraw_service(db_session, sample_account):
    result = withdraw_service("123456", 200)
    assert result["success"] is True
    assert result["new_balance"] == 300.0

    result = withdraw_service("123456", 400)  # Should fail
    assert "error" in result
    assert result["error"] == "Insufficient funds"

def test_deposit_service(db_session, sample_account):
    result = deposit_service("123456", 100)
    assert result["success"] is True
    assert result["new_balance"] == 600.0
