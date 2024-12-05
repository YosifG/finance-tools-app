from database import db
from sqlalchemy.sql import func

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    issue_date = db.Column(db.String(10))
    due_date = db.Column(db.String(10))

    for_company = db.Column(db.String(255))
    from_company = db.Column(db.String(255))

    item_name = db.Column(db.String(255))
    item_amount = db.Column(db.Integer())

    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    # TODO add better validation
    def __init__(self, issue_date, due_date, for_company, from_company, item_name, item_amount):
        self.issue_date = issue_date
        self.due_date = due_date
        self.for_company = for_company
        self.from_company = from_company
        self.item_name = item_name
        self.item_amount = item_amount