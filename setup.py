#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# Read version from app
VERSION = '0.1.0'

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme_file:
    readme = readme_file.read()

with open(os.path.join(os.path.dirname(__file__), "HISTORY.md")) as history_file:
    history = history_file.read().replace(".. :changelog:", "")

if sys.argv[-1] == "tag":
    os.system("git tag -a v{} -m 'tagging v{}'".format(VERSION, VERSION))
    os.system("git push --tags && git push origin main")
    sys.exit()

setup(
    name="botter",
    version=VERSION,
    description="""Botter bot wrapper""",
    long_description=readme + "\n\n" + history,
    author="Irving Kcam",
    author_email="irving@ramarketingconsulting.com",
    url="https://github.com/ramarketing/botter",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'selenium'
    ],
    license="Apache License 2.0",
    zip_safe=False,
    keywords="bot",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
        "Topic :: Utilities",
        "Environment :: Web Environment"
    ],
)
