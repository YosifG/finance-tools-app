from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from models.invoice_model import Invoice
from database import db
from services.invoices_service import get_invoice_service, invoice_to_dict, validate_invoice_data

invoices_api_blueprint = Blueprint("invoices", __name__)

# GET one invoice
@invoices_api_blueprint.route("/api/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoice = get_invoice_service(invoice_id)
    return jsonify(invoice_to_dict(invoice)), 200

# POST to invoices - create one invoice
# TODO move db interactions out of the route
@invoices_api_blueprint.route("/api/invoices", methods=["POST"])
def create_invoice():
    data = request.get_json()
    issue_date, due_date, for_company, from_company, item_name, item_amount = validate_invoice_data(data)

    new_invoice = Invoice(issue_date =issue_date,due_date=due_date, for_company=for_company,
                          from_company=from_company, item_name=item_name, item_amount=item_amount)
    db.session.add(new_invoice)
    db.session.commit()

    return jsonify({"message": "Invoice created", "id": new_invoice.id}), 201