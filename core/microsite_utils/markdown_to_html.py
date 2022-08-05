from core.microsite_utils.globals import *
import json
import os
from os.path import exists
import re

from datetime import datetime
from pathlib import Path
from string import ascii_letters

import markdown
from flask import abort, render_template
from icecream import ic
from markdown.extensions.toc import TocExtension


date = datetime.now().strftime('%Y')
log_date = datetime.now().strftime('%c')

def add_html(name: str) -> str:
	return name+'.html'

def add_md(name: str) -> str:
	return name+'.md'

def page_data() -> dict:
	# FIXME: This could be cleaner
	if exists(PAGEBASE) != True:
		with open(PAGEBASE, 'w') as f:
			pass
	with open(PAGEBASE, 'r') as database:
		try:
			return json.load(database)
		except json.decoder.JSONDecodeError:
			return {}

def update_database(data) -> None:
	try:
		with open(PAGEBASE, 'w') as f:
			json.dump(data, f)
	except:
		pass
	return None

def get_file_ages() -> dict:
	"""
	Get a dictionary of the latest changes to the markdown articles
	"""
	file_ages = {item:'' for item in os.listdir(PAGES)}
	for key in [key for key in file_ages if '.' in key or key == 'errors']:
		del file_ages[key] # get rid of files and the errors directory
	for dir in file_ages.keys():
		subdir, file_ages_particular = os.listdir(PAGES+dir), []
		for md_file in subdir: # find latest changes
			file_ages_particular.append(
					os.path.getmtime(PAGES+dir+'/'+md_file)
					)
		file_ages[dir] = max(file_ages_particular)
	return file_ages

def grab_title(file: str, directory: str) -> str:
	""" Find the title of the article. """
	md_location = PAGES+directory+'/'+add_md(file)
	with open(md_location, 'r') as f:
		for line in f:
			reg = r'^#\s[\d+\-\a-zA-Z]*$'
			title = re.match(reg, line)
			try:
				return title.group(0)
			except AttributeError:
				pass

def commit_to_database(file: str, directory: str) -> None:
	data = page_data()
	md_location = PAGES+directory+'/'+add_md(file)
	f = os.stat(md_location)
	try:
		title = grab_title(file=file, directory=directory).split('#')[-1].lstrip()
	except AttributeError:
		title = ''
	data.update({directory:{file:{'mod':f.st_mtime, 'title':title}}})
	update_database(data)
	return None

def build_page(file: str, directory: str) -> None:
	"""
	Create HTML file from a Markdown file 
	"""
	html_location = HTML+directory+'/'+file+'.html'
	html_loc = Path(html_location)
	html_loc.touch(exist_ok=True)
	md_location = PAGES+directory+'/'+add_md(file)
	markdown.markdownFromFile(
		input=md_location,
		output=html_location,
		extensions=[TocExtension(
			# TODO: all this will be handled by the user preferences
			permalink=False,
			title='Table of Contents',
			toc_depth="2"
		), 'footnotes']
	)
	with open(html_location, 'r+') as f:
		text = f.read()
		f.seek(0)
		f.truncate(0)
		f.write('{% extends "base.html" %}\n{% block content %}\n')
		for line in text.split('\n'):
			reg = r'^(<p><strong>\d+\. ).*(<[\"\'\\\\/]strong>)(.*)'
			line = re.sub(
				reg,
				'<div style="height: var(--space-s);"></div>'+'\n'+line,
				line
			)
			f.write(line + '\n')
		f.write('{% endblock %}' + '\n')
	commit_to_database(file=file, directory=directory)
	return None

def check_modified(file: str, directory: str) -> bool:
	""" If the file is modified, return True, else False """
	data = page_data()
	html, md = add_html(file), add_md(file)
	path_md = PAGES+directory+'/'+md
	path_html = HTML+directory+'/'+html
	if not os.path.isfile(path_html):
		if not os.path.isfile(path_md):
			# TODO: adjust this so that page is fetched from here.
			return 404
		else:
			build_page(file=file, directory=directory)
	else:
		data = page_data()
		info = os.stat(path_html)
		try:
			if info.st_mtime == data[directory][file]['mod']:
				return False
			else:
				return True
		except KeyError:
			build_page(file=file, directory=directory)
			return False

def get_title(article: str, directory: str) -> str:
	return page_data()[directory][article]['title']

def render_page(article: str, directory: str) -> list:
	"""
	Build articles from MD to HTML if not already present
	"""
	# build_menu()
	check = check_modified(file=article, directory=directory)
	if check == 404:
		return [404, directory]
	elif check == False:
		pass
	else:
		build_page(file=article, directory=directory)
	title = get_title(article=article, directory=directory)
	if len(directory) != 0:
		page_path = USER+directory+'/'
	else:
		page_path = USER
	return [
			page_path + add_html(article),
			title
			]

def markdown_checker(file: str, directory: str):
	"""
	Take the info from routes and run all the tests and functions.
	"""
	info = render_page(article=file, directory=directory)
	if info[0] == 404:
		return abort(404)
	else:
		# log_user_activity(file=file)
		# TODO: add the version number to the footer by default
		return render_template(info[0], title=info[-1].strip(), copy=date)
