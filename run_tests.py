import os
import pytest
from app import app, db  # Import the existing app and database from run.py

def reset_database():
    """Reset the database before running tests."""
    with app.app_context():
        db.drop_all()  # Clear existing tables
        db.create_all()  # Recreate tables
        print("✅ Database reset successfully!")

if __name__ == "__main__":
    reset_database()  # Ensure fresh DB before tests

    # Run all tests in the `tests/` directory
    exit_code = pytest.main(["tests/", "--disable-warnings", "-s"])

    # Exit with pytest's return code
    os._exit(exit_code)
