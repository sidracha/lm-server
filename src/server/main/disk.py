import os
from uuid import uuid4
import time
import hashlib
from flask import send_file
import pathlib

from .models import db, File
from . import vfy

#ROOT_FOLDER = os.getenv("ROOT_FOLDER")
ROOT_FOLDER = "/Users/sidrachabathuni/Projects/"

def create_file_obj(type, name, parent, path):
	print(path)
	new_file = File(id = str(uuid4()), 
					type = type,
					name = name, 
					parent = parent,
					path = path)

	return new_file

def get_db_columns(path, name, root): ## path is absolute path
	type = vfy.get_type(os.path.join(path, name))
	parent = os.path.relpath(path, root)
	if parent == ".":
		parent = ""
	f_path = os.path.relpath(os.path.join(path, name), root)
	return type, name, parent, f_path

def print_added(type, name, parent, path):
	print(type, "|", name, "|", parent, "|", path)

def populate_from_disk():
	root = ROOT_FOLDER
	x = 0
	new_file = create_file_obj("diretory", "", None, None)
	for path, dirs, files in os.walk(root):
		for dir in dirs:
			type, name, parent, f_path = get_db_columns(path, dir, root)

			new_file = create_file_obj(type, name, parent, f_path)
			print_added(type, name, parent, path)

			db.session.add(new_file)

		for file in files:
			type, name, parent, f_path = get_db_columns(path, file, root)
			new_file = create_file_obj(type, name, parent, f_path)
			print_added(type, name, parent, path)

			db.session.add(new_file)

	db.session.commit()


def get_contents(id, limit: int, offset: int): #relative path
	start_time = time.time()
	root = ROOT_FOLDER
	if id == "root":
		parent = ""
	else:
		print("here")
		dir = File.query.filter_by(id=id).first()
		if dir.type != "directory":
			return
		parent = dir.path
	
	contents = []
	files = File.query.filter_by(parent=parent).all()
	total = 0
	for f in files:
		temp_obj = {"id": f.id, "type": f.type, "name": f.name}
		contents.append(temp_obj)
		total += 1

	vfy.print_time(start_time)
	return contents[offset:limit+offset], total


def get_media_file(id):
	root = ROOT_FOLDER
	file = File.query.filter_by(id=id).first()
	abs_path = os.path.join(root, file.path)
	return send_file(abs_path)