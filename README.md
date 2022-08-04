# ⚠

## This framework is in development and should not yet be used for production. You have been warned.

---

# MicroSite

MicroSite is a Content Management Solution (CMS) wrapped around the [Flask](https://flask.palletsprojects.com/en/2.0.x/) microframework. I decided to build it after having several website-building/-maintaining jobs, and WordPress and the other solutions were either too difficult to customize appropriately, or what I was asked to provied required writing my own plugin (thank you, but no), or just seemed to slow -- rather bloated.

This project is still in its very early stages, and can just barely host its markdown files. We are working on things though, and will just go one step at a time. The python is being meticulously inspected for optimizations. Python is slow when written without a great amount of care.

The markdown syntax will be "expanded" from the standard, in order to facilitate the greater needs of a webpage. More information on the syntax will be forthcoming.

## Plugins

There are no plugins yet, but everythign is being built with plugins in mind.

## Contributing

Contributions are more than welcome.

## Development

Use a virtual environment:

```bash
pip install requirements.txt
```

If you add a python package, remember to use:

```bash
pip freeze > requirements.txt
```
Start the development server, with debugging enabled by default:

```bash
python app.py
```

Start the production server:

```bash
gunicorn -w 2 --reload app:app
```
