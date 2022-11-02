import os
from uuid import uuid4
import time

from dblayer.models import db, File

ROOT_FOLDER = "/Users/sidrachabathuni/Projects/lm-server/songs"

def populate_db():
	root = ROOT_FOLDER
	for path, dirs, files in os.walk(root):
		for file in files:
			id = str(uuid4())
			rel_path = os.path.relpath(path, root)
			print(rel_path)
			file = File(id=id, type="file", path=rel_path, name=file)
			db.session.add(file)
		for dir in dirs:
			id = str(uuid4())
			rel_path = os.path.relpath(path, root)
			print(rel_path)
			file = File(id=id, type="directory", path=rel_path, name=dir)
			db.session.add(file)
	
	db.session.commit()
	print("done")

def test():
	print(os.path.join(ROOT_FOLDER, "telugu"))

def string_search_db():
	start_time = time.time()
	q = "all"
	search = "%{}%".format(q)
	fls = []
	files = File.query.filter(File.name.like(search)).all()
	for file in files:
		fls.append(file.name)
	print(fls)
	print(f"---------{time.time() - start_time} seconds--------")

def string_search_file():
	start_time = time.time()
	q = "all"
	root = ROOT_FOLDER
	paths = []
	def recurse(directory):
		for filename in os.listdir(directory):
			if q in filename:
				paths.append(filename)
			if filename.endswith(".mp3") == False:
				recurse(os.path.join(root, directory, filename))
	
	recurse(root)
	print(paths)
	print(f"------{time.time() - start_time} seconds------")

def search3():
	start_time = time.time()
	q = "all"
	root = ROOT_FOLDER
	files = File.query.all()
	for file in files:
		if q in file.name:
			print(file.name)
