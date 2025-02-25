"""
Account Routes Module

This module defines the API routes for account-related operations,
including retrieving balances, processing deposits, and withdrawals.

It ensures proper request validation, structured error handling,
and logging of incoming HTTP requests.
"""

from flask import Blueprint, request, jsonify
from app.services.account_service import get_balance_service, withdraw_service, deposit_service
from app.utils import validate_account_number, validate_amount, format_error, format_response, log_request
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Define the blueprint for account-related routes
bp = Blueprint('account', __name__)

@bp.app_errorhandler(405)
def method_not_allowed(error):
    """
    Handles HTTP 405 Method Not Allowed errors.

    Returns:
        Response: A formatted error response indicating the method is not allowed.
    """
    return format_response(
        format_error(f"Method {request.method} not allowed for this endpoint", 405),
        success=False,
        code=405
    )

@bp.route('/')
def home():
    """
    Home page route.

    Returns:
        Response: A JSON welcome message.
    """
    logger.info("Home page accessed")
    return jsonify({"message": "Welcome to the ATM System!"}), 200

@bp.route('/accounts/<account_number>/balance', methods=['GET'])
def get_balance(account_number):
    """
    Retrieve the balance for a specified account.

    Args:
        account_number (str): The unique identifier of the account.

    Returns:
        Response: A JSON response containing the account balance or an error message.
    """
    log_request(request)  # Log the incoming request

    if not validate_account_number(account_number):
        return jsonify(format_response(format_error("Invalid account number format", 400), success=False, code=400)), 400

    result = get_balance_service(account_number)

    if "error" in result:
        return jsonify(format_response(format_error(result["error"], 404), success=False, code=404)), 404

    return jsonify(format_response(result)), 200

@bp.route('/accounts/<account_number>/withdraw', methods=['POST'])
def withdraw(account_number):
    """
    Process a withdrawal request.

    Args:
        account_number (str): The unique identifier of the account.

    Returns:
        Response: A JSON response confirming the withdrawal or an error message.
    """
    log_request(request)

    if not validate_account_number(account_number):
        return jsonify(format_response(format_error("Invalid account number format", 400), success=False, code=400)), 400

    if not request.is_json:
        return format_response(format_error("Missing JSON body or incorrect Content-Type", 415), success=False, code=415)

    data = request.get_json()
    if not data or "amount" not in data:
        return jsonify(format_response(format_error("Missing 'amount' in request body", 400), success=False, code=400)), 400

    valid, amount = validate_amount(data["amount"])
    if not valid:
        return jsonify(format_response(format_error("Invalid amount format or must be greater than zero", 400), success=False, code=400)), 400

    result = withdraw_service(account_number, amount)

    if "error" in result:
        return jsonify(format_response(format_error(result["error"], 400), success=False, code=400)), 400

    return jsonify(format_response(result)), 200

@bp.route('/accounts/<account_number>/deposit', methods=['POST'])
def deposit(account_number):
    """
    Process a deposit request.

    Args:
        account_number (str): The unique identifier of the account.

    Returns:
        Response: A JSON response confirming the deposit or an error message.
    """
    log_request(request)

    if not validate_account_number(account_number):
        return jsonify(format_response(format_error("Invalid account number format", 400), success=False, code=400)), 400

    if not request.is_json:
        return format_response(format_error("Missing JSON body or incorrect Content-Type", 415), success=False, code=415)

    data = request.get_json()
    if not data or "amount" not in data:
        return jsonify(format_response(format_error("Missing 'amount' in request body", 400), success=False, code=400)), 400

    valid, amount = validate_amount(data["amount"])
    if not valid:
        return jsonify(format_response(format_error("Invalid amount format or must be greater than zero", 400), success=False, code=400)), 400

    result = deposit_service(account_number, amount)

    if "error" in result:
        return jsonify(format_response(format_error(result["error"], 400), success=False, code=400)), 400

    return jsonify(format_response(result)), 200
