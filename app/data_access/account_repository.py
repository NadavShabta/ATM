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
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from app import db
from app.models import Account, Transaction

# Configure logging
logger = logging.getLogger(__name__)

# Global lock to prevent concurrent modifications of account balances
balance_lock = threading.Lock()


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


def update_account_balance(account_number, amount, max_retries=5):
    """
    Updates an account balance with proper locking and retry mechanisms.

    Args:
        account_number (str): The account number to update.
        amount (float): The amount to adjust the balance by (negative for withdrawals).
        max_retries (int): The maximum number of retry attempts in case of database locking.

    Returns:
        dict: A dictionary containing success status and the updated balance, or an error message.
    """
    retry_delay = 0.05  # Initial delay for retrying in case of a locked database
    session = get_session()

    for attempt in range(max_retries):
        lock_acquired = False  # Track if lock was acquired
        try:
            # Attempt to acquire the lock to prevent race conditions
            lock_acquired = balance_lock.acquire(blocking=False)
            if not lock_acquired:
                logger.warning(
                    f"Concurrent transaction detected for account {account_number}. Retry attempt {attempt + 1}/{max_retries}.")
                return {"error": "Another transaction is in progress. Please try again."}

            with session.begin():  # Ensures atomic transaction
                account = session.query(Account).filter_by(account_number=account_number).with_for_update().first()
                if not account:
                    return {"error": "Account not found"}

                if amount < 0 and account.balance < abs(amount):
                    return {"error": "Insufficient funds"}

                account.balance += amount

            return {"success": True, "account_number": account_number, "new_balance": account.balance}

        except OperationalError as e:
            session.rollback()
            if "database is locked" in str(e).lower():
                logger.warning(f"Database locked, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff to reduce contention
                continue
            return {"error": f"Database error: {e}"}

        finally:
            session.close()
            if lock_acquired:
                balance_lock.release()


def create_transaction(account_number, transaction_type, amount):
    """
    Records a transaction in the database.

    Args:
        account_number (str): The account number associated with the transaction.
        transaction_type (str): The type of transaction ('deposit' or 'withdraw').
        amount (float): The transaction amount.

    Returns:
        dict: A success message if the transaction is recorded, or an error message.
    """
    session = db.session
    try:
        account = session.query(Account).filter_by(account_number=account_number).first()
        if not account:
            return {"error": "Account not found"}

        transaction = Transaction(account_id=account.id, type=transaction_type, amount=amount)
        session.add(transaction)
        session.commit()

        logger.info(f"Transaction recorded: {transaction_type} of {amount} for account {account_number}")
        return {"success": True}

    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Transaction failed for account {account_number}: {e}")
        return {"error": f"Transaction failed: {str(e)}"}

    finally:
        session.close()
