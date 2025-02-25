"""
Utility Functions for the ATM System

This module provides helper functions for:
- Validating account numbers and transaction amounts
- Formatting API responses
- Logging incoming requests and errors
"""

import re
import logging
from flask import request

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Setup console handler if not already configured
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def validate_account_number(account_number):
    """
    Validates the format of an account number.

    A valid account number:
    - Is a non-empty string
    - Contains only digits (no letters or special characters)

    Args:
        account_number (str): The account number to validate.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not account_number:
        logger.warning("Empty account number provided.")
        return False
    if not re.fullmatch(r'\d+', account_number):
        logger.warning(f"Invalid account number format: {account_number}")
        return False
    return True


def validate_amount(amount):
    """
    Validates if the amount is a valid positive float.

    A valid amount:
    - Is a numeric value (integer or decimal)
    - Must be greater than zero

    Args:
        amount (any): The amount value to validate.

    Returns:
        tuple: (bool, float) -> True if valid, False otherwise, along with the parsed amount.
    """
    try:
        # Convert input to string and strip spaces
        raw_value = str(amount).strip()

        # Check if input is a valid numeric value
        if not re.match(r'^\d+(\.\d+)?$', raw_value):
            logger.warning(f"Invalid amount format: '{raw_value}' (Must be a valid number)")
            return False, None

        # Convert to float
        amount = float(raw_value)

        # Ensure the amount is positive
        if amount <= 0:
            logger.warning(f"Invalid amount: {amount} (Must be greater than zero)")
            return False, None

        return True, amount

    except Exception as e:
        logger.error(f"Unexpected error in validate_amount: {e}")
        return False, None


def format_error(message, code=400):
    """
    Creates a standardized error response dictionary.

    Args:
        message (str): Error message.
        code (int): HTTP status code associated with the error.

    Returns:
        dict: JSON-formatted error response.
    """
    logger.error(f"Error: {message} (Status Code: {code})")
    return {"error": message, "code": code}


def format_response(data, success=True, code=200):
    """
    Formats a standardized success response dictionary.

    Args:
        data (dict): Response data.
        success (bool): Indicates success (default: True).
        code (int): HTTP status code (default: 200).

    Returns:
        dict: JSON-formatted response.
    """
    response = {"success": success, "data": data, "code": code}
    logger.info(f"Success Response: {response}")
    return response


def log_request(req):
    """
    Logs details of an incoming HTTP request.

    Args:
        req (flask.Request): The incoming Flask request object.

    Returns:
        None
    """
    try:
        logger.info(f"Received {req.method} request for {req.url} from {req.remote_addr}")
    except Exception as e:
        logger.error(f"Error logging request: {e}")
