from .invoices_api import invoices_api_blueprint

def register_blueprints(app):
    app.register_blueprint(invoices_api_blueprint)