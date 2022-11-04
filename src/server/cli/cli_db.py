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

@db_bp.cli.command("update")
def handle_update():
	files_db.update_db()

@db_bp.cli.command("delete")
def handle_delete():
	files_db.delete_all_from_db()

@db_bp.cli.command("mp3")
def handle_mp3():
	files_db.get_mp3_under_dir("/Library")