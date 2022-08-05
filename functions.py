import json
import os
import re
from datetime import datetime
from pathlib import Path
from string import ascii_letters

import markdown
from flask import abort, render_template
from icecream import ic
from markdown.extensions.toc import TocExtension

HTML_PATH = './app/templates/articles/'
MKDN_PATH = './app/articles/'
MKDN_SECTION_PATH = './app/articles/sections/'
HTML_SECTION_PATH = './app/templates/articles/sections/'
LOGBOOK = './logbook.json'
MENU_PATH = './app/templates/menus/'

date = datetime.now().strftime('%Y')
log_date = datetime.now().strftime('%c')

def filename_html(name: str) -> str:
	return name+'.html'

def filename_md(name: str) -> str:
	return name+'.md'

def article_data() -> dict:
	with open('./articles.json', 'r') as database:
		return json.load(database)

def update_database(data) -> None:
	with open('./articles.json', 'w') as f:
		json.dump(data, f)
	return None

def get_menu_ages() -> dict:
	"""See the latest changes for the existing menus"""
	menu_ages = {x:'' for x in os.listdir(MENU_PATH)}
	for y in os.listdir(MENU_PATH):
		menu_ages[y] = os.path.getmtime(MENU_PATH+y)
	return menu_ages

def get_file_ages() -> dict:
	"""Get a dictionary of the latest changes to the markdown articles"""
	file_ages = {item:'' for item in os.listdir(MKDN_PATH)}
	for key in [key for key in file_ages if '.' in key or key == 'errors']:
		del file_ages[key] # get rid of files and the errors directory
	for dir in file_ages.keys():
		subdir, file_ages_particular = os.listdir(MKDN_PATH+dir), []
		for md_file in subdir: # find latest changes
			file_ages_particular.append(
					os.path.getmtime(MKDN_PATH+dir+'/'+md_file)
					)
		file_ages[dir] = max(file_ages_particular)
	return file_ages

def valid_sections() -> list:
	return [key for key in get_file_ages()]

def build_menu() -> None:
	"""Write menus for all articles, delete old menus"""
	menu_ages, file_ages = get_menu_ages(), get_file_ages()
	for x in file_ages.keys():
		if not x in menu_ages.keys() or file_ages[x] > menu_ages[x]:
			with open(MENU_PATH+filename_html(x), 'w') as f:
				for y in os.listdir(MKDN_PATH+x):
					f.write('<a href="{{ url_for(\'articles\', section=\'')
					f.write(x)
					f.write('\', article=\'')
					f.write(y.split('.')[0])
					f.write('\') }}">')
					f.write('PLACEHOLDER') # adjust later
					f.write('</a>\n')
	for x in menu_ages.keys():
		if x not in menu_ages.keys():
			os.remove(MENU_PATH+x)
	return None

def log_user_activity(file: str) -> None:
	"""Write user events to a file for analytics"""
	return None

def grab_title(file: str, directory: str) -> str:
	""" Find the title of the article. """
	md_location = MKDN_PATH+directory+'/'+filename_md(file)
	with open(md_location, 'r') as f:
		for line in f:
			reg = r'^#\s[\d+\-\a-zA-Z]*$'
			title = re.match(reg, line)
			try:
				return title.group(0)
			except AttributeError:
				pass

def commit_to_database(file: str, directory: str) -> None:
	data = article_data()
	md_location = MKDN_PATH+directory+'/'+filename_md(file)
	f = os.stat(md_location)
	title = grab_title(file=file, directory=directory).split('#')[-1].lstrip()
	data.update({directory:{file:{'mod':f.st_mtime, 'title':title}}})
	update_database(data)
	return None

def build_article(file: str, directory: str) -> None:
	""" Create HTML file from a mardown file """
	html_location = HTML_PATH+directory+'/'+file+'.html'
	html_loc = Path(html_location)
	html_loc.touch(exist_ok=True)
	md_location = MKDN_PATH+directory+'/'+filename_md(file)
	markdown.markdownFromFile(
		input=md_location,
		output=html_location,
		extensions=[TocExtension(
			permalink=False,
			title='Table of Contents',
			# TODO adjust the formatting of the TOC
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
	data = article_data()
	html, md = filename_html(file), filename_md(file)
	path_md = MKDN_PATH+directory+'/'+md
	path_html = HTML_PATH+directory+'/'+html
	if not os.path.isfile(path_html):
		if not os.path.isfile(path_md):
			# TODO adjust this so that page is fetched form here.
			return 404
		else:
			build_article(file=file, directory=directory)
	else:
		data = article_data()
		info = os.stat(path_html)
		try:
			if info.st_mtime == data[directory][file]['mod']:
				return False
			else:
				return True
		except KeyError:
			build_article(file=file, directory=directory)
			return False

def get_title(article: str, directory: str) -> str:
	return article_data()[directory][article]['title']

def render_article(article: str, directory: str) -> list:
	"""Build articles from MD to HTML if not already present"""
	build_menu()
	check = check_modified(file=article, directory=directory)
	if check == 404:
		return [404, directory]
	elif check == False:
		pass
	else:
		build_article(file=article, directory=directory)
		split_article(article=article, directory=directory)
	title = get_title(article=article, directory=directory)
	return ['./articles/'+directory+'/'+article+'.html', title]

def clean_section(text: str) -> str:
	"""Take out all the headings, footnotes, Jinja2 tags, etc."""
	text = re.sub('{% extends "base.html" %}', '', text, flags=re.M)
	text = re.sub('{% block content %}', '', text, flags=re.M)
	text = re.sub('{% endblock content %}', '', text, flags=re.M)
	text = re.sub('{% endblock %}', '', text, flags=re.M)
	text = re.sub(r'<div class=\"footnote\">(\n.*)*<\/div>', '', text, flags=re.M)
	text = re.sub(r"(?imsx)<h2\s.+</h2>", '', text)
	text = re.sub(r'(?imsx)<sup\sid=\"fnref:\d+\"><a\sclass=\"footnote\-ref\"\shref=\"\#fn:\d+\">\d+</a></sup>', '', text)
	return text

def make_links(file: list) -> list:
	"""Add links to the list of sections"""
	reg = r"(\d{1,4}-[a-z-]+)"
	new_file = []
	for i, text_item in enumerate(file):
		if i%2 != 0:
			new_file.append(text_item.replace('\n', ' ')) # add body at 2
		else:
			id_expanded = '#'+re.search(reg, text_item.replace('\n', '')).group()
			new_file.append(text_item)   # add header at 0
			new_file.append(id_expanded) # add link at 1
	return new_file

def split_article(article: str, directory: str) -> None:
	"""Take article and split it according to section number"""
	reg = r'(?imx)(<h3\sid=\"\d{1,4}\-[a-z\-]+\">\d{1,4}\.\s.+</h3>)'
	link_start = '<a href="{{ url_for("articles", section="'+directory+'", article="'+article+'") }}'
	link_end = '">See in Context</a>'
	with open(r''+HTML_PATH+directory+'/'+filename_html(article), 'r') as f:
		chunks = re.split(reg, f.read())
	del chunks[0] # this will always be the title/summary TODO adjust this for all use cases
	repaired_chunks = make_links(chunks)
	for part in range(0, len(repaired_chunks), 3):
		num = re.search(r'\d{1,4}', repaired_chunks[part+1], re.M|re.I)
		link = link_start+repaired_chunks[part+1]+link_end
		with open(HTML_SECTION_PATH+filename_html(num.group()), 'w+') as section:
			section.write('{% extends "base.html" %}{% block content %}\n')
			section.write(repaired_chunks[part])
			section.write(clean_section(repaired_chunks[part+2]))
			section.write(link)
			section.write('{% endblock content %}')
	return None

def valid_small_sections() -> list:
	valids = []
	for sec in os.listdir(HTML_SECTION_PATH):
		valids.append(sec)
	return valids

def markdown_checker(file: str, directory: str):
	""" take the info from routes and run all the tests and functions, """
	info = render_article(article=file, directory=directory)
	if info[0] == 404:
		return abort(404)
	else:
		log_user_activity(file=file)
		return render_template(info[0], title=info[-1].strip(), copy=date)
