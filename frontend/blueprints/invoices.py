from flask import Blueprint, render_template, request, redirect, url_for
import requests

invoices_blueprint = Blueprint("invoices_blueprint", __name__)

INVOICE_SERVICE_URL = "http://invoices:5000"

# Helper Functions
# TODO - move to a separate file
def get_invoice(invoice_id):
    """Get invoice details from the invoice service."""
    url = f"{INVOICE_SERVICE_URL}/api/invoices/{invoice_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting invoice: {e}")
        return None

def create_invoice(issue_date, due_date, for_company, from_company, item_name, item_amount):
    """Create a new invoice."""
    url = f"{INVOICE_SERVICE_URL}/api/invoices"
    data = {"issue_date": issue_date, "due_date": due_date, "for_company": for_company,
            "from_company": from_company, "item_name": item_name, "item_amount": item_amount}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating invoice: {e}")
        return None

# Routes
@invoices_blueprint.route("/invoices", methods=["GET", "POST"])
def invoices_page():
    if request.method == "POST":
        issue_date = request.form["issue_date"]
        due_date = request.form["due_date"]

        from_company = request.form["from_company"]
        for_company = request.form["for_company"]

        item_name = request.form["item_name"]
        item_amount = request.form["item_amount"]
        
        invoice = create_invoice(issue_date, due_date, for_company, from_company, item_name, item_amount)
        if invoice:
            return redirect(url_for("invoices_blueprint.invoice_page", invoice_id=invoice["id"]))
        else:
            return render_template("invoices/invoices.html", error="Failed to create invoice")
        
    return render_template("invoices/invoices.html")

@invoices_blueprint.route("/invoices/<int:invoice_id>/", methods=["GET"])
def invoice_page(invoice_id):
    invoice = get_invoice(invoice_id)
    if not invoice:
        return render_template("error.html", message="Invoice not found"), 404

    return render_template("invoices/invoice.html", invoice=invoice)