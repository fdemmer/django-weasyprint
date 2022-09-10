import logging
from pathlib import Path

import django
from django.conf import settings
from django.core.management.utils import get_random_secret_key
from django.templatetags.static import static
from django.urls import path
from django.views.generic import TemplateView

from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateView

logging.basicConfig(level=logging.DEBUG)


settings.configure(
    SECRET_KEY=get_random_secret_key(),
    ALLOWED_HOSTS=['testserver'],
    ROOT_URLCONF=__name__,
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


class BaseView(TemplateView):
    # simple Django CBV with template
    template_name = 'example.html'


class PDFDownloadView(WeasyTemplateResponseMixin, BaseView):
    # set filename for download
    pdf_filename = 'le-foo.pdf'
    # additional stylesheet(s)
    pdf_stylesheets = [static('css/print.css')]


class PDFView(WeasyTemplateView):
    template_name = 'example.html'


urlpatterns = [
    path('html/', BaseView.as_view()),
    path('pdf/', PDFView.as_view()),
    path('pdf/download/', PDFDownloadView.as_view()),
]
