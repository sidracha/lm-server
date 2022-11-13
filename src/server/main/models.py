from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class File(db.Model):
	__tablename__ = "files"

	id = db.Column(db.String, primary_key=True)
	type = db.Column(db.String, nullable=False)
	parent = db.Column(db.String, nullable=False)
	path = db.Column(db.String, nullable=False, unique=True)
	name = db.Column(db.String, nullable=False)

