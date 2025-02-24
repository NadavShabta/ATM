# # app/routes.py
#
# # Import Blueprint to group related routes, and Flask utilities to handle requests and JSON responses.
# from flask import Blueprint, request, jsonify
#
# # Import the service functions which contain our business logic.
# # These functions encapsulate operations like fetching the account balance,
# # processing a withdrawal, and processing a deposit.
# from app.services import get_balance_service, withdraw_service, deposit_service
#
# # Create a Blueprint named 'main'.
# # A Blueprint allows us to modularize our route definitions and later register them with the main app.
# bp = Blueprint('main', __name__)
#
#
# # --------------------------------------------------
# # GET /accounts/<account_number>/balance
# # --------------------------------------------------
# @bp.route('/accounts/<account_number>/balance', methods=['GET'])
# def get_balance(account_number):
#     print("im balanced")
#     """
#     Retrieves the current balance for the given account number.
#
#     Steps:
#     1. Calls the business logic function get_balance_service with the account number.
#     2. Checks if the account exists.
#     3. Returns a JSON response with the account number and its balance or an error message.
#     """
#     # Call the service function to get the account balance.
#     balance = get_balance_service(account_number)
#
#     # If the service returns None, the account was not found.
#     if balance is None:
#         return jsonify({"error": "Account not found"}), 404
#
#     # Return a successful JSON response with the account number and its balance.
#     return jsonify({"account_number": account_number, "balance": balance})
#
#
# # --------------------------------------------------
# # POST /accounts/<account_number>/withdraw
# # --------------------------------------------------
# @bp.route('/accounts/<account_number>/withdraw', methods=["POST"])
# def withdraw(account_number):
#     print('im hereee')
#     """
#     Processes a withdrawal request for the specified account.
#
#     Steps:
#     1. Extracts the JSON payload from the request.
#     2. Validates that the "amount" field is present and properly formatted.
#     3. Calls the withdraw_service to perform the withdrawal.
#     4. Returns the new balance if successful, or an error message if something goes wrong.
#     """
#     # Parse JSON data from the request body.
#     data = request.get_json()
#
#     # Validate that the request contains the required "amount" field.
#     if not data or "amount" not in data:
#         return jsonify({"error": "Missing 'amount' in request body"}), 400
#
#     # Attempt to convert the amount to a float.
#     try:
#         amount = float(data["amount"])
#     except (ValueError, TypeError):
#         return jsonify({"error": "Invalid amount format"}), 400
#
#     # Call the business logic service to process the withdrawal.
#     result = withdraw_service(account_number, amount)
#
#     # Check if the service function returned an error message.
#     if "error" in result:
#         return jsonify(result), 400
#
#     # If successful, return the updated account information.
#     return jsonify(result)
#
#
# # --------------------------------------------------
# # POST /accounts/<account_number>/deposit
# # --------------------------------------------------
# @bp.route('/accounts/<account_number>/deposit', methods=['POST'])
# def deposit(account_number):
#     """
#     Processes a deposit request for the specified account.
#
#     Steps:
#     1. Extracts the JSON payload from the request.
#     2. Validates that the "amount" field is provided and correctly formatted.
#     3. Calls the deposit_service to add funds to the account.
#     4. Returns the updated balance or an error if the operation fails.
#     """
#     # Parse JSON data from the request body.
#     data = request.get_json()
#
#     # Validate that the request includes the "amount" field.
#     if not data or "amount" not in data:
#         return jsonify({"error": "Missing 'amount' in request body"}), 400
#
#     # Attempt to convert the deposit amount to a float.
#     try:
#         amount = float(data["amount"])
#     except (ValueError, TypeError):
#         return jsonify({"error": "Invalid amount format"}), 400
#
#     # Call the service function to process the deposit.
#     result = deposit_service(account_number, amount)
#
#     # Check if the service function returned an error message.
#     if "error" in result:
#         return jsonify(result), 400
#
#     # Return a successful JSON response with updated account details.
#     return jsonify(result)


# app/routes.py

from flask import Blueprint, request, jsonify
from app.services import get_balance_service, withdraw_service, deposit_service

bp = Blueprint('main', __name__)


@bp.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    print(f"Fetching balance for {account_number}")

    balance = get_balance_service(account_number)

    if balance is None:
        return jsonify({"error": "Account not found"}), 404

    return jsonify({"account_number": account_number, "balance": balance})


@bp.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    print(f"Processing withdrawal for account {account_number}")

    data = request.get_json()

    if not data or "amount" not in data:
        return jsonify({"error": "Missing 'amount' in request body"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount format"}), 400

    result = withdraw_service(account_number, amount)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)


@bp.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    print(f"Processing deposit for account {account_number}")

    data = request.get_json()

    if not data or "amount" not in data:
        return jsonify({"error": "Missing 'amount' in request body"}), 400

    try:
        amount = float(data["amount"])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount format"}), 400

    result = deposit_service(account_number, amount)

    if "error" in result:
        return jsonify(result), 400

    return jsonify(result)

