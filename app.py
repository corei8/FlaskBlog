from core import app

if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
    # momentjs = application.jinja_env.globals['momentjs']
