from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../../../files.sqlite3"

from dblayer.models import db
db.init_app(app)
with app.app_context():
	db.create_all()

from cli.cli_db import db_bp
app.register_blueprint(db_bp)



@app.route("/")
def handle_home():
	return "hello world"

if __name__ == "__main__":
	app.run()