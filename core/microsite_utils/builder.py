# import os
from os import listdir, mkdir
from re import sub

def get_all_pages():
	"""
	Generates a list of all the markdown pages for the website.
	"""
	try:
		pages = listdir('pages/')
	except FileNotFoundError:
		mkdir('./pages/')
		pages = listdir('pages/')
	return pages

def check_valid_name(name: str) -> str:
	"""
	Ensures that the names for the markdown files will be easy to 
	work with: no numbers, spaces, special characters, etc.
	"""
	if len(name) == 0:
		valid_name = 'untitled'
	else: valid_name = name.lower()
	return valid_name
