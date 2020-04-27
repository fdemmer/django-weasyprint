from pathlib import Path

from setuptools import find_packages, setup

VERSION = '0.6.0'
github_url = 'https://github.com/fdemmer/django-weasyprint'


setup(
    name='django-weasyprint',
    version=VERSION,
    author='Florian Demmer',
    author_email='fdemmer@gmail.com',
    description='Django WeasyPrint CBV',
    long_description=(Path(__file__).parent.resolve() / 'README.rst').read_text(),
    download_url=f'{github_url}/archive/v{VERSION}.tar.gz',
    url=github_url,
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
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    setup_requires=['wheel'],
    install_requires=[
        'Django>=2.2',
        'WeasyPrint>=43',
    ],
)
