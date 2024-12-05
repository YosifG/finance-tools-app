from .payment_links import payment_links_blueprint
from .invoices import invoices_blueprint

def register_blueprints(app):
    app.register_blueprint(payment_links_blueprint)
    app.register_blueprint(invoices_blueprint)