from os import listdir, mkdir, remove
from re import sub

from core.microsite_utils.globals import *

def check_valid_name(name: str) -> str:
	"""
	Ensures that the names for the markdown files will be easy to 
	work with: no numbers, spaces, special characters, etc.
	"""
	if len(name) == 0:
		valid_name = 'untitled'
	else: valid_name = name.lower()
	return valid_name

def add_markdown_page(filename: str) -> None:
	""" 
	Make a file in the pages/ directory with the filename being the 
	input.
	"""
	open(PAGES+check_valid_name(filename)+'.md', 'a').close()
	return None

def get_all_pages():
	"""
	Generates a list of all the markdown pages for the website.
	"""
	try:
		dirty_pages= listdir('pages/')
	except FileNotFoundError:
		mkdir('./pages/')
		dirty_pages = listdir('pages/') # FIXME make this cleaner -> its always len 0
	if len(dirty_pages) == 0: # make sure that there is a home file
		add_markdown_page('home')
		dirty_pages= listdir('pages/')
	pages = [ page.split('.')[0] for page in dirty_pages ]
	return pages


def delete_page(page: str) -> None:
	"""
	Delete the page provided from the pages/ directory.
	"""
	remove('pages/'+page+'.md')
	return None
