from core import app

if __name__ == '__main__':
    app.jinja_env.cache = {}
    app.run(host='127.0.0.1', debug=True, use_reloader=True)
    # momentjs = application.jinja_env.globals['momentjs']
