from werkzeug.exceptions import NotFound, BadRequest
from models.payment_link_model import PaymentLink
import requests
from flask import jsonify
import logging
import re

logger = logging.getLogger(__name__)

def get_payment_link_service(payment_link_id):
    """Gets a payment link ."""
    payment_link = PaymentLink.query.get(payment_link_id)
    if not payment_link:
        raise NotFound(f"Payment link with ID {payment_link_id} not found.")
    return payment_link

def payment_link_to_dict(payment_link):
    """Converts a PaymentLink object to a dictionary."""
    return {
        "id": payment_link.id,
        "amount": payment_link.amount,
        "status": payment_link.status,
        "email": payment_link.email
    }

#TODO add email format validation
def validate_payment_link_data(data):
    if not data or not data.get("amount"):
        raise BadRequest("Amount is required.")
    if not data.get("email"):
        raise BadRequest("Email is required.")
    try:
        amount = float(data["amount"])
    except ValueError:
        raise BadRequest("Amount is required.")
    return amount, data["email"]

#TODO better error handling
def send_payment_link_email(payment_link):
    email = payment_link.email
    amount = payment_link.amount

    lambda_url = "https://odqvtaciue3vaqhvm2dilngrci0mesqs.lambda-url.eu-north-1.on.aws/"
    payload = {
        "email": email,
        "payment_amount": amount
    }
    try:
        response = requests.post(lambda_url, json=payload)

        if response.status_code == 200:
            logger.info("Payment confirmation email sent successfully.")
        else:
            logger.error(f"Failed to send payment email. Status: {response.status_code}, Response: {response.text}")

    except requests.exceptions.RequestException as e:
        return jsonify({
            "message": "An error occurred while sending the payment confirmation email",
            "error": str(e)
        }), 500

