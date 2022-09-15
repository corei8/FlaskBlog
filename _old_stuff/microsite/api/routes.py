from datetime import *
from time import perf_counter

from flask import abort, render_template, request, redirect, url_for
from flask_optimize import FlaskOptimize

from microsite.microsite_utils.builder import get_all_pages, check_valid_name, delete_page, add_markdown_page
from microsite.microsite_utils.globals import *
from microsite.microsite_utils.markdown_to_html import markdown_checker

# from microsite import app
# from functions import (markdown_checker, render_article, valid_sections,
                       # valid_small_sections)
from microsite import create_app

app = create_app()

flask_optimize = FlaskOptimize()

date = datetime.now().strftime('%Y')

@app.route("/home", strict_slashes=False)
@flask_optimize.optimize()
def landing_page():
	try:
		return markdown_checker('home', '')
	except FileNotFoundError:
		return render_template('microsite_default_welcome.html') 

@app.route("/") # NOTE: just for now
@app.route("/login", strict_slashes=False)
@flask_optimize.optimize()
def admin_login():
	if request.method == 'POST':
		pass
	return render_template('builder.html')

@app.route("/builder", strict_slashes=False, methods=['POST', 'GET'])
@flask_optimize.optimize()
def builder():
	if request.method == 'POST':
		if 'add_page_form' in request.form:
			filename = request.form['new_page']
			add_markdown_page(filename)
		elif 'page_to_delete' in request.form:
			delete_page(request.form['page_to_delete'])
		else:
			abort(500)
	return render_template(
			'builder/dashboard.html',
			pages_list = get_all_pages(),
			)

@app.route("/edit_page", strict_slashes=True, methods=['POST', 'GET'])
@flask_optimize.optimize()
def edit_page():
	if request.method == 'POST':
		if 'edited_content' in request.form:
			file = request.form['edited_file']
			content = request.form['edited_content']
			with open(PAGES+file, 'w') as f:
				f.truncate(0)
				f.write(request.form['edited_content'])
			# write to the file and continue edit session?
			with open(PAGES+file, 'r') as f:
				file_content = f.read()
			return render_template(
				'builder/page_editor.html',
				content=file_content,
				filename = file,
				)
		else:
			file = request.form['page_to_edit']
			# prevent adding '.md' if no change to file:
			if file.split('.')[-1] == 'md':
				pass
			else:
				file += '.md'
			with open(PAGES+file, 'r') as f:
				file_content = f.read()
			return render_template(
					'builder/page_editor.html',
					content=file_content,
					filename = file,
					)

# @app.route("/<section>/<string:article>", methods=['GET'], strict_slashes=False)
# @flask_optimize.optimize()
# def articles(section, article):
	# if not section in valid_sections():
		# return abort(404)
	# else:
		# return markdown_checker(file=article, directory=section)

# @app.route("/<int:section>", methods=['GET'], strict_slashes=False)
# @flask_optimize.optimize()
# def sections(section):
	# section_template = 'articles/sections/'+str(section)+'.html'
	# if not str(section)+'.html' in valid_small_sections():
		# return abort(404)
	# else:
		# return render_template(section_template, title='', copy=date, section=True)

