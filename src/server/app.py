import os
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__, template_folder="../client/templates", static_folder="../client/static")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../../../files.sqlite3"

from main.models import db
db.init_app(app)
with app.app_context():
	db.create_all()

from cli.main_cli import db_bp
app.register_blueprint(db_bp)

from main import files

@app.route("/")
def handle_home():
	return render_template("index.html")


@app.route("/sub")
def handle_sub():
	args = request.args
	path = args["path"]
	if path == "/":
		path = ""
	contents, total = files.get_contents(path, int(args["limit"]), int(args["offset"]))
	return jsonify({"contents": contents, "total": total})

#test_path = "/Users/sidrachabathuni/Projects/lm-server/songs/english/britney/Britney Spears - Toxic (Official HD Video).mp3"
@app.route("/mp3")
def handle_mp3():
	args = request.args
	path = args["path"]
	abs_path = files.get_abs_path(path)
	return send_file(abs_path)

@app.route("/test")
def handle_test():
	files.test()
	return "done"

if __name__ == "__main__":
	app.run()