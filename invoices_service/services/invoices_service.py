from werkzeug.exceptions import NotFound, BadRequest
from models.invoice_model import Invoice

def get_invoice_service(invoice_id):
    """Get an invoice from the database."""

    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        raise NotFound(f"Invoice with ID {invoice_id} not found.")
    return invoice

def invoice_to_dict(invoice):
    """Converts an Invoice object to a dictionary."""

    return {
        "id": invoice.id,

        "issue_date": invoice.issue_date,
        "due_date": invoice.due_date,

        "for_company": invoice.for_company,
        "from_company": invoice.from_company,

        "item_name": invoice.item_name,
        "item_amount": invoice.item_amount,
    }

# TODO improve validatoion, e.g. issue_date must be before due_date.
def validate_invoice_data(data):
    """Validates invoice data"""
    if not data or not data.get("issue_date"):
        raise BadRequest("Issue date required.")
    if not data.get("due_date"):
        raise BadRequest("Due date required.")
    if not data.get("for_company"):
        raise BadRequest("Receiving company required.")
    if not data.get("from_company"):
        raise BadRequest("Sending company required.")
    if not data.get("item_name"):
        raise BadRequest("Item name required.")
    if not data.get("item_amount"):
        raise BadRequest("Item amount required.")
    
    return data["issue_date"], data["due_date"], data["for_company"], data["from_company"], data["item_name"], data["item_amount"]