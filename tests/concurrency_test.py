import requests
import multiprocessing
import time

BASE_URL = "http://127.0.0.1:5000"
ACCOUNT_NUMBER = "123456"
NUM_PROCESSES = 10  # Adjust as needed
DEPOSIT_AMOUNT = 100
WITHDRAW_AMOUNT = 50


def deposit():
    """Send a deposit request and print raw response before JSON parsing."""
    response = requests.post(
        f"{BASE_URL}/accounts/{ACCOUNT_NUMBER}/deposit",
        json={"amount": DEPOSIT_AMOUNT},
    )
    print(f"Raw Deposit Response: {response.status_code} - {response.text}")  # Debug
    try:
        print(f"Deposit Response: {response.json()}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")


def withdraw():
    """Send a withdrawal request and print raw response before JSON parsing."""
    response = requests.post(
        f"{BASE_URL}/accounts/{ACCOUNT_NUMBER}/withdraw",
        json={"amount": WITHDRAW_AMOUNT},
    )
    print(f"Raw Withdraw Response: {response.status_code} - {response.text}")  # Debug
    try:
        print(f"Withdraw Response: {response.json()}")
    except Exception as e:
        print(f"Error decoding JSON: {e}")


def test_concurrent_transactions():
    """Run deposits and withdrawals concurrently."""
    processes = []
    for _ in range(NUM_PROCESSES // 2):
        p = multiprocessing.Process(target=deposit)
        processes.append(p)

    for _ in range(NUM_PROCESSES // 2):
        p = multiprocessing.Process(target=withdraw)
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("\nAll transactions completed.")


if __name__ == "__main__":
    start_time = time.time()
    test_concurrent_transactions()
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")
