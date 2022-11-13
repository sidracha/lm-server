from flask import Blueprint

from main import disk

db_bp = Blueprint("db", __name__)

@db_bp.cli.command("setup")
def handle_setup():
	disk.populate_from_disk()