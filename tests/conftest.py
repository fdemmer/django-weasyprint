import logging
from pathlib import Path

import django
from django.conf import settings
from django.core.management.utils import get_random_secret_key
from django.urls import path
from django.views.generic import TemplateView

from django_weasyprint import (
    WeasyTemplateResponse,
    WeasyTemplateResponseMixin,
    WeasyTemplateView,
)


# Test views
class BaseView(TemplateView):
    template_name = 'example.html'


class PDFDownloadView(WeasyTemplateResponseMixin, BaseView):
    pdf_filename = 'le-foo.pdf'
    pdf_stylesheets = ['/static/css/print.css']
    pdf_options = {'pdf_version': '1.6'}


class PDFView(WeasyTemplateView):
    template_name = 'example.html'


def pdf_view(request):
    return WeasyTemplateResponse(request, 'example.html', {})


# URL patterns for tests
urlpatterns = [
    path('html/', BaseView.as_view()),
    path('pdf/', PDFView.as_view()),
    path('pdf/view/', pdf_view),
    path('pdf/download/', PDFDownloadView.as_view()),
]


def pytest_configure():
    logging.basicConfig(level=logging.DEBUG)

    settings.configure(
        DEBUG=False,
        SECRET_KEY=get_random_secret_key(),
        ALLOWED_HOSTS=['testserver'],
        ROOT_URLCONF=__name__,  # Use this module as the URL conf
        INSTALLED_APPS=['django.contrib.staticfiles'],
        STATIC_URL='/static/',
        STATIC_ROOT='/www/static',
        MIDDLEWARE=[],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [Path(__file__).parent / 'templates'],
        }],
        DATABASES={'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }},
    )
    django.setup()
