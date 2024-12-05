import os
from flask import Flask
from werkzeug.exceptions import BadRequest
from database import db
from blueprints import register_blueprints
from errors import handle_not_found, handle_bad_request 

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object("config.Config")

db.init_app(app)

register_blueprints(app)

app.register_error_handler(404, handle_not_found)
app.register_error_handler(BadRequest, handle_bad_request)