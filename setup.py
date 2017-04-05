from setuptools import setup

setup(
    name='django-weasyprint',
    version='0.1',
    description='Django weasyprint app',
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
        "django >= 1.4",
        "WeasyPrint",
    ],
)
