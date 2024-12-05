from database import db
from sqlalchemy.sql import func

class PaymentLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(), default = "Unpaid")
    email = db.Column(db.String())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    #TODO email format validation
    def __init__(self, amount, email):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.amount = amount
        self.status = "Unpaid"
        self.email = email