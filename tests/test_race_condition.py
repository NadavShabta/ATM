import threading
import pytest
from sqlalchemy import text
from app import app, db
from app.services.account_service import withdraw_service
from app.models import Account

@pytest.fixture(scope="function")
def setup_account():
    """
    Set up a test account in the database before each test.
    """
    with app.app_context():
        db.session.execute(text("DELETE FROM accounts"))  # Ensure a clean slate
        db.session.commit()
        account = Account(account_number="123456", balance=500.0)
        db.session.add(account)
        db.session.commit()
        yield account
        db.session.rollback()  # Ensure test isolation

def withdraw_thread(results, index):
    """
    Worker function to perform a withdrawal in a separate thread.
    """
    with app.app_context():
        result = withdraw_service("123456", 100)  # Attempt to withdraw 100
        results[index] = result

def test_race_condition(setup_account):
    """
    Test concurrent withdrawals with 10 threads.
    Expected outcome: Around 5 should succeed.
    """
    num_threads = 10  # 10 concurrent withdrawal attempts
    results = [None] * num_threads  # Store results

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=withdraw_thread, args=(results, i))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    success_count = sum(1 for res in results if res and res.get("success"))
    failure_count = num_threads - success_count

    print(f"✅ Successful Withdrawals: {success_count}")
    print(f"❌ Failed Withdrawals (Insufficient Funds): {failure_count}")

    assert 4 <= success_count <= 6, f"Expected ~5 successful withdrawals, got {success_count}"
    assert 4 <= failure_count <= 6, f"Expected ~5 failed withdrawals, got {failure_count}"
