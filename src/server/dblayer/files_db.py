import os
from uuid import uuid4
import time

from dblayer.models import db, File

#ROOT_FOLDER = "/Users/sidrachabathuni/Projects/lm-server/songs"
ROOT_FOLDER = "/Users/sidrachabathuni/Projects"

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
			print(f"-------{start_time-time.time()}------")
	
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


def get_contents(directory): #relative path
	if len(directory) != 0:
		if directory[0] == "/":
			directory = directory[1:]
	start_time = time.time()
	root = ROOT_FOLDER
	contents = []
	print("directory", directory)
	for x in os.listdir(os.path.join(root, directory)):
		abs_path = os.path.join(root, directory, x)
		rel_path = os.path.relpath(abs_path, root)

		if os.path.isdir(abs_path):
			content_obj = {"name": x, "type": "directory"}
		else:
			content_obj = {"name": x, "type": "file"}
		
		contents.append(content_obj)
		#file = File.query.filter_by(path=rel_path).first()
		#try:
			#content_obj = {"id": file.id, "path": file.path, "type": file.type}
			#contents.append(content_obj)
		#except:
			#continue
	print(f"------{start_time-time.time()} seconds------")
	return contents

def test():
	start_time = time.time()
	ids = ["35c663a5-30e5-47e3-8336-cdc8accbc575", "23282ea7-e561-454a-8bd1-f266c3007fb3", "7a7ea9aa-abdc-4b9f-8587-a4841f27bf0a"]
	for id in ids:
		file = File.query.filter_by(id=id).first()
		print(file.name)
	
	print(f"------{start_time-time.time()} seconds------")