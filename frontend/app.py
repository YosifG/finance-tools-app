
from flask import Flask, render_template
from blueprints import register_blueprints

app = Flask(__name__)

register_blueprints(app)

# TODO move errors to separate file
@app.errorhandler(404)
def handle_not_found(error):
    return render_template("error.html", message="Page not found"), 404

@app.errorhandler(Exception)
def handle_exception(error):
    return render_template("error.html", message="An unexpected error occurred"), 500

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def home():
    return render_template("home.html")