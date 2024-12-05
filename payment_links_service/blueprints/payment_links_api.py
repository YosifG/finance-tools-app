from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from models.payment_link_model import PaymentLink
from database import db
from services.payment_links_service import get_payment_link_service, payment_link_to_dict, send_payment_link_email, validate_payment_link_data

payment_links_api_blueprint = Blueprint("payment_links", __name__)

# GET one payment link
@payment_links_api_blueprint.route("/api/payment-links/<int:payment_link_id>", methods=["GET"])
def get_payment_link(payment_link_id):
    payment_link = get_payment_link_service(payment_link_id)
    return jsonify(payment_link_to_dict(payment_link)), 200

# POST payment-links - create a new payment link
# TODO move db interactions out of the route
@payment_links_api_blueprint.route("/api/payment-links", methods=["POST"])
def create_payment_link():
    data = request.get_json()
    amount, email = validate_payment_link_data(data)
    
    new_payment_link = PaymentLink(amount=amount, email=email)
    db.session.add(new_payment_link)
    db.session.commit()

    send_payment_link_email(new_payment_link)

    return jsonify({"message": "Payment link created", "id": new_payment_link.id}), 201

# Pay a payment link
# TODO Implement a CC portal and update status based on it
@payment_links_api_blueprint.route("/api/payment-links/<int:payment_link_id>/pay", methods=["POST"])
def pay_payment_link(payment_link_id):
    payment_link = get_payment_link_service(payment_link_id)
    payment_link.status = "PAID"
    db.session.commit()

    return jsonify({"message": "Payment link Paid successfully"}), 201