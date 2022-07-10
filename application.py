from app import application

if __name__ == '__main__':
    application.jinja_env.cache = {}
    application.run(host='0.0.0.0', threading=True, debug=True)
    # momentjs = application.jinja_env.globals['momentjs']
