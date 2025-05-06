"""
Account Repository Module

This module handles database interactions related to accounts and transactions.
It provides functions to retrieve account details, update account balances with
proper concurrency handling, and log transactions.

It ensures safe database operations using SQLAlchemy,
including row-level locking for balance updates to prevent race conditions.
"""

import logging
import time
import threading
import random
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app import db
from app.models import Account, Transaction
from sqlalchemy.exc import OperationalError
from my_app import get_session, logger



# Configure logging
logger = logging.getLogger(__name__)

def get_session():
    """
    Creates and returns a new scoped session for database operations.

    Returns:
        scoped_session: A new SQLAlchemy session bound to the application's database engine.
    """
    return scoped_session(sessionmaker(bind=db.engine))


def get_account(account_number, for_update=False):
    """
    Retrieves an account from the database by its account number.

    Args:
        account_number (str): The unique identifier of the account.
        for_update (bool): If True, applies a row-level lock on the retrieved account.

    Returns:
        Account | None: The retrieved account object if found, otherwise None.
    """
    session = get_session()
    try:
        query = session.query(Account).filter_by(account_number=account_number)
        if for_update:
            query = query.with_for_update()
        return query.first()
    finally:
        session.close()




def perform_transaction(account_number, amount, transaction_type, max_retries=5):
    """
    Performs a transaction (withdrawal or deposit) atomically, updating Accounts and Transactions.
    
    Args:
        account_number (str): The account number.
        amount (float): The amount to adjust (negative for withdrawal, positive for deposit).
        transaction_type (str): 'withdraw' or 'deposit'.
        max_retries (int): Maximum retry attempts for database contention.
    
    Returns:
        dict: Success status, new balance, or error message.
    """
    retry_delay = 0.05
    session = get_session()
    for attempt in range(max_retries):
        try:
            with session.begin():  # Single transaction for both operations
                # Update balance with row-level locking
                account = session.query(Account).filter_by(account_number=account_number).with_for_update().first()
                if not account:
                    return {"error": "Account not found"}
                if amount < 0 and account.balance < abs(amount):
                    return {"error": "Insufficient funds"}
                account.balance += amount
                # Create transaction
                transaction = Transaction(account_id=account.id, type=transaction_type, amount=abs(amount))
                session.add(transaction)
            logger.info(f"Transaction {transaction_type} of {abs(amount)} for account {account_number} completed")
            return {"success": True, "account_number": account_number, "new_balance": account.balance}
        except OperationalError as e:
            session.rollback()
            if "database is locked" in str(e).lower():
                logger.warning(f"Database contention for account {account_number}, attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_delay + random.uniform(0, 0.01))
                retry_delay *= 2
                continue
            return {"error": f"Database error: {e}"}
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Transaction failed for account {account_number}: {e}")
            return {"error": f"Transaction failed: {str(e)}"}
    return {"error": "Max retries exceeded due to database contention"}
