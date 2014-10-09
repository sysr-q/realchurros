"""
"""
from setuptools import setup

kw = {
	"name": "realchurros",
	"version": "0.1.0",
	"description": "",
	"long_description": __doc__,
	"url": "https://github.com/sysr-q/realchurros",
	"author": "sysr-q",
	"author_email": "chris@gibsonsec.org",
	"license": "MIT",
	"packages": [
		"realchurros",
	],
	"package_dir": {
		"realchurros": "realchurros",
	},
	"install_requires": [
		"gevent",
		"twitter",
		"parsedatetime",
	],
	"zip_safe": False,
}

if __name__ == "__main__":
	setup(**kw)
