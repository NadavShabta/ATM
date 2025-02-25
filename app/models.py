"""
Database Models for the ATM System

This module defines the database models for the ATM system, including:
- `Account`: Represents a bank account with an account number and balance.
- `Transaction`: Represents a deposit or withdrawal transaction linked to an account.

These models are managed by SQLAlchemy.
"""

from datetime import datetime
from app import db

class Account(db.Model):
    """
    Represents a bank account in the system.

    Attributes:
        id (int): Primary key for the account.
        account_number (str): Unique account identifier.
        balance (float): Current balance of the account.
        transactions (relationship): One-to-many relationship to `Transaction`.

    Methods:
        __repr__(): Returns a string representation of the account.
    """
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    # Relationship to transactions
    transactions = db.relationship('Transaction', backref='account', lazy=True)

    def __repr__(self):
        return f'<Account {self.account_number} - Balance: {self.balance}>'


class Transaction(db.Model):
    """
    Represents a financial transaction (deposit or withdrawal) associated with an account.

    Attributes:
        id (int): Primary key for the transaction.
        account_id (int): Foreign key linking to an account.
        type (str): Indicates the transaction type ('deposit' or 'withdraw').
        amount (float): The amount involved in the transaction.
        timestamp (datetime): The time when the transaction was created.

    Methods:
        __repr__(): Returns a string representation of the transaction.
    """
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'deposit' or 'withdraw'
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transaction {self.id} - {self.type} {self.amount} on {self.timestamp}>'
