# -*- coding: utf-8 -*-
import codecs
import os

from setuptools import find_packages, setup

VERSION = '0.5.5'
github_url = 'https://github.com/fdemmer/django-weasyprint'


def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file. Assume UTF-8 encoding.
    """
    pwd = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(pwd, *parts), 'rb', 'utf-8') as f:
        return f.read()


setup(
    name='django-weasyprint',
    version=VERSION,
    description='Django WeasyPrint CBV',
    long_description=read('README.rst'),
    url=github_url,
    download_url=github_url + '/archive/v{0}.tar.gz'.format(VERSION),
    author='Florian Demmer',
    author_email='fdemmer@gmail.com',
    license='Apache-2.0',
    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Framework :: Django",
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    install_requires=[
        'Django==1.11;python_version<="2.7"',
        'cairocffi==0.9.0;python_version<="2.7"',
        'tinycss2==0.6.1;python_version<="2.7"',
        'WeasyPrint==0.42.3;python_version<="2.7"',
        'Django>=2.2;python_version>="3.6"',
        'WeasyPrint>=43;python_version>="3.6"',
    ],
)
