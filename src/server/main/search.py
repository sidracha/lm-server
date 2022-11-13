from .models import File
from . import vfy
import time
import os
from thefuzz import fuzz, process

from .disk import ROOT_FOLDER

def fuzzy_search(q): #very expensive? 
	start_time = time.time()
	files = File.query.all()
	fls = []
	for file in files:
		if fuzz.partial_token_set_ratio(q, file.name) == 100:
			f_obj = {"path": file.path, "type": file.type}
			fls.append(f_obj)
	
	vfy.print_time(start_time)

	return fls, time.time() - start_time
	

def fuzzy_search_files(q):
	root = ROOT_FOLDER
	start_time = time.time()
	fls = []
	def fuzzy(file, path):
		if fuzz.partial_token_set_ratio(q, file) == 100:	
			rel_path = os.path.relpath(os.path.join(path, file), root)
			f_obj = {"path": rel_path, "type": vfy.get_type(file)}
			return f_obj
		else:
			return False
	for path, dirs, files in os.walk(root):
		for file in files:
			res = fuzzy(file, path)
			if res == False:
				continue
			fls.append(fuzzy(file, path))
		for dir in dirs:
			res = fuzzy(dir, path)
			if res == False:
				continue
			fls.append(fuzzy(dir, path))

	vfy.print_time(start_time)
	print(fls)
	return fls, time.time()-start_time


def search(q: str):
	q = "%{}%".format(q.lower())
	start_time = time.time()
	fls = []
	files = File.query.filter(File.name.like(q)).all()
	for file in files:
		fls.append(file.path)
	vfy.print_time(start_time)

	return fls, time.time() - start_time


def search_files(q):
	root = ROOT_FOLDER
	fls = []
	start_time = time.time()
	q = q.lower()
	for path, dirs, files in os.walk(root):
		for file in files:
			if q in file.lower():
				fls.append(os.path.join(path, file))
		for dir in dirs:
			if q in dir.lower():
				fls.append(os.path.join(path, dir))

	vfy.print_time(start_time)
	return fls, time.time()-start_time
