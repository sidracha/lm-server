import os
from uuid import uuid4
import time

from .models import db, File
from . import ignore

ROOT_FOLDER = os.getenv("ROOT_FOLDER")

def populate_db():
	root = ROOT_FOLDER
	for path, dirs, files in os.walk(root):
		for file in files:
			if ignore.check(file) == 0:
				continue
			id = str(uuid4())
			rel_path = os.path.relpath(path, root)
			if rel_path == ".":
				rel_path = ""
			print(os.path.join(rel_path, file))
			file = File(id=id, type="file", path=os.path.join(rel_path, file), name=file)
			db.session.add(file)
		for dir in dirs:
			id = str(uuid4())
			rel_path = os.path.relpath(path, root)
			if rel_path == ".":
				rel_path = ""
			print(os.path.join(rel_path, dir))
			file = File(id=id, type="directory", path=os.path.join(rel_path, dir), name=dir)
			db.session.add(file)
	
	db.session.commit()
	print("done")


def string_search_db():
	start_time = time.time()
	q = "all the stars"#
	search = "%{}%".format(q)
	fls = []
	files = File.query.filter(File.name.like(search)).all()
	for file in files:
		fls.append(file.name)
	print(fls)
	print(f"---------{time.time() - start_time} seconds--------")



def update_db():
	test = File.query.first()
	if bool(test) == False:
		print("you need to run flask db populate first")
		return
	root = ROOT_FOLDER
	for path, dirs, files in os.walk(root):
		for dir in dirs:
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

			rp = os.path.relpath(path, root)
			if rp == ".":
				rp = ""
			rel_path = os.path.join(rp, file)

			fls = File.query.filter_by(path=rel_path, name=file).first()
			if bool(fls) == False:
				id = str(uuid4())
				new_file = File(id=id, type="file", path=rel_path, name=file)
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
		if ignore.check(x) == 0:
			continue
		abs_path = os.path.join(root, directory, x)
		rel_path = os.path.relpath(abs_path, root)

		if os.path.isdir(abs_path):
			type = "directory"
		else:
			if x.endswith(".mp3"):
				type = "mp3"
			else:
				type = "file"
				
		content_obj = {"name": x, "type": type}

		
		contents.append(content_obj)
		total += 1

	print(f"------{start_time-time.time()} seconds------")
	return contents[offset:limit+offset], total

def test():
	start_time = time.time()
	ids = ["35c663a5-30e5-47e3-8336-cdc8accbc575", "23282ea7-e561-454a-8bd1-f266c3007fb3", "7a7ea9aa-abdc-4b9f-8587-a4841f27bf0a"]
	for id in ids:
		file = File.query.filter_by(id=id).first()
		print(file.name)
	
	print(f"------{start_time-time.time()} seconds------")


def get_abs_path(rel_path):
	root = ROOT_FOLDER
	if rel_path[0] == "/":
		rel_path = rel_path[1:]
	
	return os.path.join(root, rel_path)