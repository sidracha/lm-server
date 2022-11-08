import os
import pathlib
import time

def ignore(name):
	if name == ".DS_Store":
		return 0

def get_type(name):
	support = [".mp3", ".mp4", ".mov", ".wav"]
	suffix = pathlib.Path(name).suffix
	if suffix == "":
		return "directory"
	elif suffix in support:
		return "media"
	else:
		return "file"

def print_time(start_time):
	print(f"------{time.time() - start_time} seconds------")
