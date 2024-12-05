import pytest
from werkzeug.exceptions import BadRequest
from services.payment_links_service import  validate_payment_link_data

# Basic tests of validate_payment_link service
# TODO Implement an app factory then write more comprehensive tests that require Flask app
## such as whether status is automatically set to Unpaid

def test_validate_payment_links_data_valid_data():
    """
    Test validate_payment_link_data with valid data.
    """
    data = {
        "amount": 1000,
        "email": "acme@gmail.com"
    }
    result = validate_payment_link_data(data)
    assert result == (
        1000.0,
        "acme@gmail.com"
    )

def test_validate_payment_link_data_missing_fields():
    """
    Test validate_payment_link_data with missing fields.
    """
    data = {
        #missing amount
        "status": "Unpaid",
        "email": "acme@gmail.com"
    }
    with pytest.raises(BadRequest, match="Amount is required."):
        validate_payment_link_data(data)

def test_validate_invoice_data_empty_data():
    """
    Test validate_invoice_data with empty data.
    """
    with pytest.raises(BadRequest, match="Amount is required."):
        validate_payment_link_data({})