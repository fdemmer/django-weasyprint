from setuptools import setup

readme = open('README.rst').read()

setup(
    name='django-weasyprint',
    version='0.4',
    description='Django weasyprint app',
    long_description=readme,
    url='https://github.com/fdemmer/django-weasyprint',
    author='Florian Demmer',
    author_email='fdemmer@gmail.com',
    license='Apache-2.0',
    classifiers=[
        "Framework :: Django",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python',
    ],
    packages=['django_weasyprint'],
    package_data={
        'django_weasyprint': [],
    },
    install_requires=[
        "Django >= 1.4",
        "WeasyPrint",
    ],
)
