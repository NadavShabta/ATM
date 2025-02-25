import pytest
from app.data_access.account_repository import get_account, update_account_balance, create_transaction
from app.models import Account

def test_get_account(db_session, sample_account):
    account = get_account("123456")
    assert account is not None
    assert account.account_number == "123456"

def test_update_account_balance(db_session, sample_account):
    result = update_account_balance("123456", 100)
    assert result["success"] is True
    assert result["new_balance"] == 600.0

    result = update_account_balance("123456", -700)  # Should fail
    assert "error" in result
    assert result["error"] == "Insufficient funds"

def test_create_transaction(db_session, sample_account):
    """
    Test creating a transaction for an account.
    """
    result = create_transaction(sample_account.account_number, "deposit", 100.0)

    # Ensure transaction was successfully created
    assert result == {"success": True}, f"Expected success message, got {result}"

