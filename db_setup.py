"""
Database Setup and Initialization

This module is responsible for ensuring that the database is properly set up.
It creates the necessary tables and populates sample data if the database is empty.
"""

from app import db
from app.models import Account

def initialize_database():
    """
    Ensures the database schema is created and initializes it with sample data if empty.

    This function:
    - Creates all necessary database tables.
    - Checks if sample accounts exist.
    - If no accounts are found, it populates the database with 10 sample accounts.

    The function is designed to be called during application startup.
    """
    with db.session.begin():  # Ensures atomic database transactions
        db.create_all()  # Creates tables if they do not already exist

        # Check if the database already contains accounts
        if not Account.query.first():
            print("Populating the database with sample accounts...")
            accounts = [
                Account(account_number=f"1000{i}", balance=1000.0 * i)
                for i in range(1, 11)
            ]
            db.session.bulk_save_objects(accounts)  # Efficient bulk insert
            db.session.commit()
            print("10 sample accounts created successfully!")
        else:
            print("Database already initialized. No new accounts added.")
