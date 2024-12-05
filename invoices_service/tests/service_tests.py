import pytest
from werkzeug.exceptions import BadRequest
from services.invoices_service import  validate_invoice_data

# Basic tests of validate_invoice_data service
# TODO Implement an app factory then write more comprehensive tests that require Flask app

def test_validate_invoice_data_valid_data():
    """
    Test validate_invoice_data with valid data.
    """
    data = {
        "issue_date": "01-01-2024",
        "due_date": "01-01-2024",
        "for_company": "ACME",
        "from_company": "EMCA",
        "item_name": "Coding service",
        "item_amount": 1000
    }
    result = validate_invoice_data(data)
    assert result == (
        "01-01-2024",
        "01-01-2024",
        "ACME",
        "EMCA",
        "Coding service",
        1000
    )

def test_validate_invoice_data_missing_fields():
    """
    Test validate_invoice_data with missing fields.
    """
    data = {
        "issue_date": "01-01-2024",
        "due_date": "01-01-2024",
        "for_company": "ACME",
        # No from_company
        "item_name": "Coding service",
        "item_amount": 1000
    }
    with pytest.raises(BadRequest, match="Sending company required."):
        validate_invoice_data(data)

def test_validate_invoice_data_empty_data():
    """
    Test validate_invoice_data with empty data.
    """
    with pytest.raises(BadRequest, match="Issue date required."):
        validate_invoice_data({})