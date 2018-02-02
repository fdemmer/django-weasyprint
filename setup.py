from setuptools import find_packages, setup

readme = open('README.rst').read()

setup(
    name='django-weasyprint',
    version='0.4',
    long_description=readme,
    description='Django WeasyPrint CBV',
    url='https://github.com/fdemmer/django-weasyprint',
    download_url='https://github.com/fdemmer/django-weasyprint/archive/v{0}.tar.gz'.format(VERSION),
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
        "Django>=1.8",
        "WeasyPrint",
    ],
)
