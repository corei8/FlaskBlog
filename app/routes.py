from datetime import *
from time import perf_counter

from flask import abort, render_template
from flask_optimize import FlaskOptimize
from icecream import ic, install

from app import application
from functions import (markdown_checker, render_article, valid_sections,
                       valid_small_sections)

ic.configureOutput(prefix='==> ') # eye-candy for icecream
install() # to use ic() for debugging globally.

flask_optimize = FlaskOptimize()

date = datetime.now().strftime('%Y')

@application.route("/")
@application.route("/home", strict_slashes=False)
@flask_optimize.optimize()
def landing_page():
	return markdown_checker('home', '')

@application.route("/<section>/<string:article>", methods=['GET'], strict_slashes=False)
@flask_optimize.optimize()
def articles(section, article):
	if not section in valid_sections():
		return abort(404)
	else:
		return markdown_checker(file=article, directory=section)

@application.route("/<int:section>", methods=['GET'], strict_slashes=False)
@flask_optimize.optimize()
def sections(section):
	section_template = 'articles/sections/'+str(section)+'.html'
	if not str(section)+'.html' in valid_small_sections():
		return abort(404)
	else:
		return render_template(section_template, title='', copy=date, section=True)

# TODO keep the error pages in another page
@application.errorhandler(404)
@flask_optimize.optimize()
def page_not_found(e):
	info = render_article(article='404', directory='errors')
	return render_template(info[0], title=info[-1], copy=date), 404

@application.errorhandler(500)
@flask_optimize.optimize()
def page_not_found(e):
	info = render_article(article='500', directory='errors')
	return render_template(info[0], title=info[-1], copy=date), 500
