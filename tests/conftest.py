
import pytest
from app import create_app, db

@pytest.fixture(scope="session")
def app():
    """
    Create and configure a new app instance for testing.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # Use an in-memory DB for tests
    return app

@pytest.fixture(scope="session")
def client(app):
    """
    Flask test client for making HTTP requests in tests.
    """
    return app.test_client()

@pytest.fixture(scope="function")
def db_session(app):
    """
    Initialize a new database session per test.
    """
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def sample_account(db_session):
    """
    Create a sample account for testing.
    """
    from app.models import Account
    account = Account(account_number="123456", balance=500.0)
    db_session.add(account)
    db_session.commit()
    return account
