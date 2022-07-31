# MicroSite

Small tool built with Python and Flask for building static websites with
Markdown.

## How does it work?

This website uses the microframework [Flask](https://flask.palletsprojects.com/en/2.0.x/).

## How to use this?

Word on this later...

### How do we get the articles as HTML?

The articles are interpreted markdown files.

## Contributing

Contributions are welcome.

## Development

Use a virtual environment:

```bash
pip install requirements.txt
```

If you add a python package, remember to use:

```bash
pip freeze > requirements.txt
```

Start the server:

```bash
gunicorn -w 2 --reload application:application
```
