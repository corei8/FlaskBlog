from datetime import *
from time import perf_counter

from flask import abort, render_template, request
from flask_optimize import FlaskOptimize
from icecream import ic, install

from core.microsite_utils.builder import get_all_pages

from core import app
# from functions import (markdown_checker, render_article, valid_sections,
                       # valid_small_sections)

ic.configureOutput(prefix='==> ') # eye-candy for icecream
install() # to use ic() for debugging globally.

flask_optimize = FlaskOptimize()

date = datetime.now().strftime('%Y')

# # @app.route("/")
# @app.route("/home", strict_slashes=False)
# @flask_optimize.optimize()
# def landing_page():
	# return markdown_checker('home', '')

@app.route("/")
@app.route("/builder", strict_slashes=False)
@flask_optimize.optimize()
def builder():
	return render_template('builder.html')

PAGES = 'pages/'

@app.route("/builder_home", strict_slashes=False, methods=['POST', 'GET'])
@flask_optimize.optimize()
def builder_home():
	if request.method == 'POST':
		# TODO add flag for return type
		file = request.form['page_to_edit']
		with open(PAGES+file, 'r') as f:
			file_content = f.read()
		return render_template(
				'builder_home.html',
				page_view = 'edit_page',
				content=file_content
				)
	return render_template(
			'builder_home.html',
			pages_list = get_all_pages(),
			page_view = 'menu',
			)

@app.route("/add_page", strict_slashes=True, methods=['POST', 'GET'])
def add_page():
	if request.method == 'POST':
		filename = request.form['new_page']
		open(PAGES+filename+'.md', 'a').close() # create the file
		return render_template(
				'builder_home.html',
				pages_list = get_all_pages(),
				page_view = 'menu'
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

# # TODO keep the error pages in another page
# @app.errorhandler(404)
# @flask_optimize.optimize()
# def page_not_found(e):
	# info = render_article(article='404', directory='errors')
	# return render_template(info[0], title=info[-1], copy=date), 404

# @app.errorhandler(500)
# @flask_optimize.optimize()
# def page_not_found(e):
	# info = render_article(article='500', directory='errors')
	# return render_template(info[0], title=info[-1], copy=date), 500
