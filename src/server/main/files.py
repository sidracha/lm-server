import os
from uuid import uuid4
import time
import hashlib

from .models import db, File
from . import vfy

#ROOT_FOLDER = os.getenv("ROOT_FOLDER")
ROOT_FOLDER = "/Users/sidrachabathuni/"


def populate_db():
	root = ROOT_FOLDER
	count = 0
	for path, dirs, files in os.walk(root):
		for file in files:
			count += 1
			if vfy.ignore(file) == 0:
				continue
			rel_path = os.path.relpath(path, root)
			if rel_path == ".":
				rel_path = ""
			id = str(uuid4())
			print(os.path.join(rel_path, file))
			type = vfy.get_type(file)
			file = File(id=id, type=type, path=os.path.join(rel_path, file), name=file)
			db.session.add(file)
		for dir in dirs:
			count += 1
			id = str(uuid4())
			rel_path = os.path.relpath(path, root)
			if rel_path == ".":
				rel_path = ""
			print(os.path.join(rel_path, dir))
			file = File(id=id, type="directory", path=os.path.join(rel_path, dir), name=dir)
			db.session.add(file)
	
	db.session.commit()
	print("done")
	print(count)






def update_db():
	test = File.query.first()
	if bool(test) == False:
		print("you need to run flask db populate first")
		return
	root = ROOT_FOLDER
	for path, dirs, files in os.walk(root):
		for dir in dirs:
			if vfy.ignore(dir) == 0:
				continue
			print(dir)
			rp = os.path.relpath(path, root)
			if rp == ".":
				rp = ""
			rel_path = os.path.join(rp, dir)
			drs = File.query.filter_by(path=rel_path, name=dir).first()
			if bool(drs) == False:
				id = str(uuid4())
				new_file = File(id=id, type="directory", path=rel_path, name=dir)
				db.session.add(new_file)
				print(f"added {dir}")
		for file in files:
			if vfy.ignore(file) == 0:
				continue
			rp = os.path.relpath(path, root)
			if rp == ".":
				rp = ""
			rel_path = os.path.join(rp, file)
			fls = File.query.filter_by(path=rel_path, name=file).first()
			if bool(fls) == False:
				type = vfy.get_type(file)
				id = str(uuid4())
				new_file = File(id=id, type=type, path=rel_path, name=file)
				db.session.add(new_file)
				print(f"added {file}")
		
	db.session.commit()
	

	files = File.query.all()
	for file in files:
		abs_path = os.path.join(root, file.path)
		start_time = time.time()
		if os.path.exists(abs_path) == False:
			File.query.filter_by(path=file.path).delete()
			print(f"deleted {file.name}")
			print(file.path)
			print(f"-------{start_time-time.time()}------")
	
	db.session.commit()
	print("done!")

def repopulate():
	delete_all_from_db()
	populate_db()
				
def delete_all_from_db():
	File.query.delete()
	try:
		db.session.commit()
	except:
		db.session.rollback()
	
	print("done!")


def get_mp3_under_dir(directory): #directory is relative path
	root = ROOT_FOLDER
	fls = []
	limit = 100
	start_time = time.time()
	abs_path = os.path.join(root, directory)
	for path, dirs, files in os.walk(abs_path):
		for file in files:
			#if file.endswith(".mp3"):
			rel_path = os.path.relpath(os.path.join(path, file), root)
			fls.append(rel_path)
			limit -=1
	
	print(fls)
	print(f"------{time.time() - start_time} seconds------")
	return fls


def get_contents(directory, limit: int, offset: int): #relative path
	if len(directory) != 0:
		if directory[0] == "/":
			directory = directory[1:]
	start_time = time.time()
	root = ROOT_FOLDER
	contents = []
	print("directory", directory)
	total = 0
	for x in os.listdir(os.path.join(root, directory)):
		if vfy.ignore(x) == 0:
			continue
		abs_path = os.path.join(root, directory, x)
		rel_path = os.path.relpath(abs_path, root)

		if os.path.isdir(abs_path):
			type = "directory"
		else:
			type = vfy.get_type(x)	
		content_obj = {"name": x, "type": type}

		
		contents.append(content_obj)
		total += 1

	print(f"------{start_time-time.time()} seconds------")
	return contents[offset:limit+offset], total


def get_abs_path(rel_path):
	root = ROOT_FOLDER
	if rel_path[0] == "/":
		rel_path = rel_path[1:]
	
	return os.path.join(root, rel_path)
