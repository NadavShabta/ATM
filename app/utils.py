# app/utils.py

"""
This module provides utility functions for the ATM system.
It includes helper functions for validating inputs, formatting error responses,
and logging request details to assist in debugging and monitoring.
"""

import re
import logging

# Configure a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Setup console handler with a simple formatter if not already configured
if not logger.handlers:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def validate_account_number(account_number):
    """
    Validates the format of an account number.

    For this ATM system, a valid account number is defined as a non-empty string
    containing only digits. This validation rule can be extended based on specific requirements.

    Args:
        account_number (str): The account number to validate.

    Returns:
        bool: True if the account number is valid, False otherwise.
    """
    if not account_number:
        logger.warning("Empty account number provided.")
        return False
    # Use a regular expression to check that the account number consists solely of digits.
    if not re.fullmatch(r'\d+', account_number):
        logger.warning("Invalid account number format: %s", account_number)
        return False
    return True


def format_error(message, code=400):
    """
    Creates a standardized error response dictionary.

    This function helps in centralizing error response formatting so that
    all endpoints return errors in a consistent structure.

    Args:
        message (str): A descriptive error message.
        code (int): An HTTP status code associated with the error.

    Returns:
        dict: A dictionary containing the error message and code.
    """
    logger.error("Error occurred: %s (Status Code: %d)", message, code)
    return {"error": message, "code": code}


def log_request(request):
    """
    Logs details about an incoming HTTP request.

    This function can be used to record basic request information,
    which can be invaluable for debugging or monitoring system usage.

    Args:
        request (flask.Request): The incoming Flask request object.

    Returns:
        None
    """
    logger.info("Received %s request for %s from %s", request.method, request.url, request.remote_addr)
