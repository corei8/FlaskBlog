from setuptools import setup

setup(
    name='microsite',
	version = "0.0.1",
    author = "Gregory Robert Barnes",
    author_email = "corei8.github@gmail.com",
    packages=['microsite'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
	classifiers=[
        "Development Status :: 1 - Planning",
    ],
)
