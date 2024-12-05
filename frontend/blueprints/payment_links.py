from flask import Blueprint, render_template, request, redirect, url_for
import requests

payment_links_blueprint = Blueprint("payment_links_blueprint", __name__)

PAYMENT_LINK_SERVICE_URL = "http://payment_links:5000"

# Helper Functions
# TODO move to a separate file
def get_payment_link(payment_link_id):
    """Get payment link details from the payment link service."""
    url = f"{PAYMENT_LINK_SERVICE_URL}/api/payment-links/{payment_link_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting payment link: {e}")
        return None

def create_payment_link(amount, email):
    """Create a new payment link."""
    url = f"{PAYMENT_LINK_SERVICE_URL}/api/payment-links"
    data = {"amount": amount, "email": email}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error creating payment link: {e}")
        return None

def update_payment_link_status(payment_link_id):
    """Update the status of a payment link."""
    url = f"{PAYMENT_LINK_SERVICE_URL}/api/payment-links/{payment_link_id}/pay"
    try:
        response = requests.post(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error updating payment link status: {e}")
        return None

# Routes
@payment_links_blueprint.route("/payment-links", methods=["GET", "POST"])
def payment_links_page():
    if request.method == "POST":
        amount = request.form["amount"]
        email = request.form["email"]
        
        payment_link = create_payment_link(amount, email)
        if payment_link:
            return redirect(url_for("payment_links_blueprint.payment_link_page", payment_link_id=payment_link["id"]))
        else:
            return render_template("payment_links/payment_links.html", error="Failed to create payment link")

    return render_template("payment_links/payment_links.html")

@payment_links_blueprint.route("/payment-links/<int:payment_link_id>/", methods=["GET"])
def payment_link_page(payment_link_id):
    payment_link = get_payment_link(payment_link_id)
    if not payment_link:
        return render_template("error.html", message="Payment link not found"), 404

    return render_template("payment_links/payment_link.html", payment_link=payment_link)

@payment_links_blueprint.route("/payment-links/<int:payment_link_id>/pay", methods=["POST"])
def pay_payment_link(payment_link_id):
    updated_link = update_payment_link_status(payment_link_id)
    if updated_link:
        return redirect(url_for("payment_links_blueprint.payment_link_page", payment_link_id=payment_link_id))
    else:
        return render_template("error.html", message="Failed to update payment link status"), 400