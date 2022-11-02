from genericpath import exists
from logging import RootLogger
import os
from posixpath import relpath
from re import I
from uuid import uuid4
import time

from dblayer.models import db, File

ROOT_FOLDER = "/Users/sidrachabathuni/Projects/lm-server/songs"
#ROOT_FOLDER = "/Users/sidrachabathuni"

def populate_db():
	root = ROOT_FOLDER
	for path, dirs, files in os.walk(root):
		for file in files:
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
		for dir in dirs:
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
	db.session.commit()
	

	files = File.query.all()
	for file in files:
		abs_path = os.path.join(root, file.path)
		if os.path.exists(abs_path) == False:
			File.query.filter_by(path=file.path).delete()
			print(f"deleted {file.name}")
	
	db.session.commit()
	print("done!")
				
def delete_all_from_db():
	print("are you sure you want to delete the database?(y/n)")
	inpt = input("> ")
	if inpt != "y":
		return
	File.query.delete()
	try:
		db.session.commit()
	except:
		db.session.rollback()
	
	print("done!")
	