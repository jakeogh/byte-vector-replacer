# -*- coding: utf-8 -*-

import sys

from setuptools import find_packages
from setuptools import setup

import fastentrypoints

dependencies = ["click"]

config = {
    "version": "0.1",
    "name": "byte_vector_replacer",
    "url": "https://github.com/jakeogh/byte-vector-replacer",
    "license": "ISC",
    "author": "Justin Keogh",
    "author_email": "github.com@v6y.net",
    "description": "manages and applies dict of automatically replaced byte vectors in ~/.config",
    "long_description": __doc__,
    "packages": find_packages(exclude=["tests"]),
    "package_data": {"byte_vector_replacer": ["py.typed"]},
    "include_package_data": True,
    "zip_safe": False,
    "platforms": "any",
    "install_requires": dependencies,
    "entry_points": {
        "console_scripts": [
            "byte-vector-replacer=byte_vector_replacer.byte_vector_replacer:cli",
        ],
    },
}

setup(**config)
