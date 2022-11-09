import os
import pathlib
import time


def ignore(name):
	if name == ".DS_Store":
		return True

def get_type(path):
	support = [".mp3", ".mp4", ".mov", ".wav"]
	suffix = pathlib.Path(path).suffix
	path = os.path.join("/Users/sidrachabathuni", path)
	print(path, os.path.isdir(path))
	if os.path.isdir(path) == True:
		return "directory"
	elif suffix in support:
		return "media"
	else:
		return "file"

def print_time(start_time):
	print(f"------{time.time() - start_time} seconds------")
