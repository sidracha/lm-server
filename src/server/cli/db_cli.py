from flask import Blueprint

from main import files

db_bp = Blueprint("db", __name__)


@db_bp.cli.command("setup")
def handle_setup():
	print("hello, world")

@db_bp.cli.command("populate")
def handle_populate():
	files.populate_db()

@db_bp.cli.command("test")
def handle_test():
	files.test()

@db_bp.cli.command("search")
def handle_search():
	files.string_search_db()

@db_bp.cli.command("update")
def handle_update():
	files.update_db()

@db_bp.cli.command("delete")
def handle_delete():
	print("are you sure you want to delete the database?(y/n)")
	inpt = input("> ")
	if inpt != "y":
		return
	files.delete_all_from_db()

@db_bp.cli.command("mp3")
def handle_mp3():
	files.get_mp3_under_dir("/Library")

@db_bp.cli.command("repopulate")
def handle_repopulate():
	files.repopulate()