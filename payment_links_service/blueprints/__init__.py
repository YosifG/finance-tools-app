from .payment_links_api import payment_links_api_blueprint

def register_blueprints(app):
    app.register_blueprint(payment_links_api_blueprint)