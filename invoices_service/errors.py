from werkzeug.exceptions import BadRequest
from flask import jsonify

def handle_not_found(error):
    return jsonify({"error": "Resource not found"}), 404

def handle_bad_request(error):
    return jsonify({"error": str(error)}), 400