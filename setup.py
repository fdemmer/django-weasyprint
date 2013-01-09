from setuptools import setup

setup(
    name='django-weasyprint',
    version='0.1',
    description='Django weasyprint app',
    author='Jeroen Dekkers',
    author_email='jeroen@dekkes.ch',
    classifiers=[
        "Framework :: Django",
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python',
    ],
    packages=['django_weasyprint'],
    package_data={
        'django_weasyprint': [
            'locale/*/LC_MESSAGES/*'
        ],
    },
    install_requires=[
        "django >= 1.4",
        "WeasyPrint",
    ],
)
