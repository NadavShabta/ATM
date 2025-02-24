import unittest
import json
from app import create_app, db
from app.models import Account


class ATMSystemTestCase(unittest.TestCase):
    """
    Test case for the ATM system API.

    This class contains unit tests for the ATM system's API endpoints, including
    balance retrieval, deposits, and withdrawals. It uses an in-memory SQLite
    database for testing purposes.
    """

    def setUp(self):
        """
        Set up the test environment before each test case runs.
        """
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create all database tables

            # Add test accounts
            account1 = Account(account_number='123456', balance=1000.0)
            account2 = Account(account_number='654321', balance=500.0)
            db.session.add(account1)
            db.session.add(account2)
            db.session.commit()

    def tearDown(self):
        """
        Clean up the test environment after each test case runs.
        """
        with self.app.app_context():
            db.drop_all()

    def test_get_balance_success(self):
        """
        Test that a valid GET request to retrieve the account balance returns
        the expected balance and account number.
        """
        response = self.client.get('/accounts/123456/balance')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["balance"], 1000.0)
        self.assertEqual(data["account_number"], "123456")

    def test_get_balance_account_not_found(self):
        """
        Test that a GET request for a non-existent account returns a 404 error.
        """
        response = self.client.get('/accounts/000000/balance')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_withdraw_success(self):
        """
        Test a successful withdrawal operation.
        """
        payload = json.dumps({"amount": 100})
        response = self.client.post(
            '/accounts/123456/withdraw',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["new_balance"], 900.0)
        self.assertEqual(data["account_number"], "123456")

    def test_withdraw_insufficient_funds(self):
        """
        Test that a withdrawal request with an amount exceeding the account's
        balance returns an error.
        """
        payload = json.dumps({"amount": 2000})
        response = self.client.post(
            '/accounts/123456/withdraw',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_withdraw_invalid_amount(self):
        """
        Test that a withdrawal request with an invalid (non-positive) amount
        returns an error.
        """
        payload = json.dumps({"amount": -50})
        response = self.client.post(
            '/accounts/123456/withdraw',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_withdraw_zero_amount(self):
        """
        Test that a withdrawal request with a zero amount returns an error.
        """
        payload = json.dumps({"amount": 0})
        response = self.client.post(
            '/accounts/123456/withdraw',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_deposit_success(self):
        """
        Test a successful deposit operation.
        """
        payload = json.dumps({"amount": 200})
        response = self.client.post(
            '/accounts/654321/deposit',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data["new_balance"], 700.0)
        self.assertEqual(data["account_number"], "654321")

    def test_deposit_invalid_amount(self):
        """
        Test that a deposit request with an invalid (non-positive) amount returns an error.
        """
        payload = json.dumps({"amount": -20})
        response = self.client.post(
            '/accounts/654321/deposit',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_deposit_zero_amount(self):
        """
        Test that a deposit request with a zero amount returns an error.
        """
        payload = json.dumps({"amount": 0})
        response = self.client.post(
            '/accounts/654321/deposit',
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


if __name__ == '__main__':
    unittest.main()