from pathlib import Path

from setuptools import find_packages, setup

VERSION = '1.1.0'
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
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    setup_requires=['wheel'],
    install_requires=[
        'Django>=2.2',
        'WeasyPrint>=43',
    ],
)
