import os
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../../../files.sqlite3"

from dblayer.models import db
db.init_app(app)
with app.app_context():
	db.create_all()

from cli.cli_db import db_bp
app.register_blueprint(db_bp)

from dblayer import files_db

@app.route("/")
def handle_home():
	return render_template("index.html")


@app.route("/sub")
def handle_sub():
	args = request.args
	path = args["path"]
	if path == "/":
		path = ""
	contents = files_db.get_contents(path)
	return jsonify({"contents": contents})


@app.route("/test")
def handle_test():
	files_db.test()
	return "done"

if __name__ == "__main__":
	app.run()