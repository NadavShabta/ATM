"""
Account Service Module

This module handles business logic for account-related operations,
including retrieving balances, processing withdrawals, and deposits.

It interacts with the `account_repository.py` to perform database
transactions and ensures validation, error handling, and logging.
"""

import logging
from app.data_access.account_repository import update_account_balance, create_transaction, get_account
from sqlalchemy.exc import SQLAlchemyError
from app.utils import validate_account_number, validate_amount, format_error

# Configure logging
logger = logging.getLogger(__name__)

def get_balance_service(account_number):
    """
    Retrieve the current balance for the given account number.

    Args:
        account_number (str): Unique identifier for the account.

    Returns:
        dict: A dictionary containing the account number and balance, or an error message.
    """
    logger.info(f"Fetching balance for account {account_number}")

    if not validate_account_number(account_number):
        return format_error("Invalid account number format", 400)

    try:
        account = get_account(account_number)  # Fetch account from repository
        if not account:
            return format_error("Account not found", 404)

        return {"success": True, "account_number": account_number, "balance": account.balance}

    except SQLAlchemyError as e:
        logger.error(f"Database error while fetching balance for account {account_number}: {e}")
        return format_error("A database error occurred", 500)

def withdraw_service(account_number, amount):
    """
    Process a withdrawal request with validation and proper handling.

    Args:
        account_number (str): The unique account number.
        amount (float): Amount to withdraw.

    Returns:
        dict: A success message with the updated balance or an error message.
    """
    logger.info(f"Processing withdrawal for account {account_number}, amount: {amount}")

    # Validate inputs
    if not validate_account_number(account_number):
        return format_error("Invalid account number format", 400)

    valid, amount = validate_amount(amount)
    if not valid:
        return format_error("Invalid amount format or must be greater than zero", 400)

    try:
        # Perform withdrawal via the repository (handles locking & balance check)
        result = update_account_balance(account_number, -amount)
        if "error" in result:
            return result  # Return error from repository

        # Log transaction
        create_transaction(account_number, 'withdraw', amount)

        logger.info(f"Withdrawal successful for account {account_number}, new balance: {result['new_balance']}")
        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error during withdrawal for account {account_number}: {e}")
        return format_error("A database error occurred during withdrawal", 500)
    except Exception as e:
        logger.error(f"Unexpected error during withdrawal for account {account_number}: {e}")
        return format_error("An unexpected error occurred", 500)

def deposit_service(account_number, amount):
    """
    Process a deposit with validation and proper handling.

    Args:
        account_number (str): The unique account number.
        amount (float): Amount to deposit.

    Returns:
        dict: A success message with the updated balance or an error message.
    """
    logger.info(f"Processing deposit for account {account_number}, amount: {amount}")

    # Validate inputs
    if not validate_account_number(account_number):
        return format_error("Invalid account number format", 400)

    valid, amount = validate_amount(amount)
    if not valid:
        return format_error("Invalid amount format or must be greater than zero", 400)

    try:
        # Perform deposit via the repository (handles locking)
        result = update_account_balance(account_number, amount)
        if "error" in result:
            return result  # Return error from repository

        # Log transaction
        create_transaction(account_number, 'deposit', amount)

        logger.info(f"Deposit successful for account {account_number}, new balance: {result['new_balance']}")
        return result

    except SQLAlchemyError as e:
        logger.error(f"Database error during deposit for account {account_number}: {e}")
        return format_error("A database error occurred during deposit", 500)
    except Exception as e:
        logger.error(f"Unexpected error during deposit for account {account_number}: {e}")
        return format_error("An unexpected error occurred", 500)
