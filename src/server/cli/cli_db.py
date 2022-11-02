from importlib.metadata import files
from flask import Blueprint

from dblayer import files_db

db_bp = Blueprint("db", __name__)

@db_bp.cli.command("populate")
def handle_populate():
	files_db.populate_db()

@db_bp.cli.command("test")
def handle_test():
	files_db.test()

@db_bp.cli.command("search")
def handle_search():
	files_db.string_search_db()

@db_bp.cli.command("search2")
def handle_search2():
	files_db.string_search_file()