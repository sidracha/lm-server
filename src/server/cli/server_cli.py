from flask import Blueprint

from main import files

server_bp = Blueprint("server", __name__)

@server_bp.cli.command("setup")
def handle_setup():
	files.setup()