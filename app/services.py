#
#
# from app.models import Account
# from app import db
#
#
# def get_balance_service(account_number):
#     """
#     Retrieves the current balance for the given account number.
#
#     Args:
#         account_number (str): Unique identifier for the account.
#
#     Returns:
#         float: The account's balance if the account exists.
#         None: If the account is not found.
#     """
#     # Retrieve the account from the database
#     account = Account.query.filter_by(account_number=account_number).first()
#
#     if not account:
#         return None  # Account not found
#
#     return account.balance  # Return balance from database
#
#
# def withdraw_service(account_number, amount):
#     """
#     Processes a withdrawal request.
#
#     Args:
#         account_number (str): The unique account number.
#         amount (float): Amount to withdraw.
#
#     Returns:
#         dict: A success message with the updated balance or an error message.
#     """
#     account = Account.query.filter_by(account_number=account_number).first()
#
#     if not account:
#         return {"error": "Account not found"}
#
#     if amount <= 0:
#         return {"error": "Withdrawal amount must be greater than 0"}
#
#     if account.balance < amount:
#         return {"error": "Insufficient funds"}
#
#     # Deduct the amount and commit the change
#     account.balance -= amount
#     db.session.commit()
#
#     return {"account_number": account_number, "new_balance": account.balance}
#
#
# def deposit_service(account_number, amount):
#     """
#     Processes a deposit for a given account.
#
#     Args:
#         account_number (str): Unique identifier for the account.
#         amount (float): Amount to deposit.
#
#     Returns:
#         dict: A success message with the updated balance or an error message.
#     """
#     account = Account.query.filter_by(account_number=account_number).first()
#
#     if not account:
#         return {"error": "Account not found"}
#
#     if amount <= 0:
#         return {"error": "Deposit amount must be greater than 0"}
#
#     # Add deposit and save to DB
#     account.balance += amount
#     db.session.commit()
#
#     return {"account_number": account_number, "new_balance": account.balance}
#




import logging
from datetime import datetime
from app.models import Account, Transaction
from app import db
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def get_balance_service(account_number):
    """
    Retrieves the current balance for the given account number.

    Args:
        account_number (str): Unique identifier for the account.

    Returns:
        dict: A dictionary containing the account number and balance, or an error message.
    """
    logger.info(f"Fetching balance for account {account_number}")
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        logger.warning(f"Account {account_number} not found")
        return {"error": "Account not found"}
    return {"account_number": account_number, "balance": account.balance}




def withdraw_service(account_number, amount):
    """
    Processes a withdrawal request.

    Args:
        account_number (str): The unique account number.
        amount (float): Amount to withdraw.

    Returns:
        dict: A success message with the updated balance or an error message.
    """
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return {"error": "Account not found"}

    if amount <= 0:
        return {"error": "Withdrawal amount must be greater than 0"}

    if account.balance < amount:
        return {"error": "Insufficient funds"}

    try:
        account.balance -= amount
        transaction = Transaction(account_id=account.id, type='withdraw', amount=amount, timestamp=datetime.utcnow())
        db.session.add(transaction)
        db.session.commit()
        return {"account_number": account_number, "new_balance": account.balance}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during withdrawal: {e}")
        return {"error": "An error occurred during withdrawal"}


def deposit_service(account_number, amount):
    """
    Processes a deposit for a given account.
    """
    account = Account.query.filter_by(account_number=account_number).first()
    if not account:
        return {"error": "Account not found"}

    if amount <= 0:
        return {"error": "Deposit amount must be greater than 0"}

    try:
        # Update account balance
        account.balance += amount

        # Create a deposit transaction
        transaction = Transaction(account_id=account.id, type='deposit', amount=amount, timestamp=datetime.utcnow())
        db.session.add(transaction)
        db.session.commit()

        return {"account_number": account_number, "new_balance": account.balance}
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during deposit: {e}")
        return {"error": "An error occurred during deposit"}