#!/usr/bin/env python

import os
from setuptools import setup, find_packages
import commando


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as source:
        return source.read()


setup(
    name="django-commando",
    version=commando.__version__,
    description="A declarative API for writing, overriding and sequencing Django management commands",
    long_description=read("README"),
    author="Mike Kibbel",
    author_email="mkibbel@gmail.com",
    url="https://github.com/skibblenybbles/django-commando",
    license="MIT License",
    platforms=["OS Independent"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    packages=find_packages(exclude=["example", "example.*"]),
    install_requires=[
        "Django>=1.4",
    ],
)
