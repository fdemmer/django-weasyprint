from pathlib import Path

from setuptools import find_packages, setup


VERSION = '2.3.1'
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
    project_urls={
        'Changelog': f'{github_url}/blob/v{VERSION}/CHANGELOG.md',
    },
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    python_requires='>=3.8',
    setup_requires=['wheel'],
    install_requires=[
        'Django>=3.2',
        'WeasyPrint>=59',
    ],
)
