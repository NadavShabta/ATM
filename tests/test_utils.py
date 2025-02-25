import pytest
from app.utils import validate_account_number, validate_amount, format_error, format_response

def test_validate_account_number():
    assert validate_account_number("12345") is True
    assert validate_account_number("abc123") is False
    assert validate_account_number("") is False

def test_validate_amount():
    assert validate_amount(100) == (True, 100.0)
    assert validate_amount("50.5") == (True, 50.5)
    assert validate_amount("-10") == (False, None)
    assert validate_amount("invalid") == (False, None)

def test_format_error():
    response = format_error("Test Error", 400)
    assert response == {"error": "Test Error", "code": 400}

def test_format_response():
    response = format_response({"message": "Success"}, success=True, code=200)
    assert response["success"] is True
    assert response["data"] == {"message": "Success"}
    assert response["code"] == 200
