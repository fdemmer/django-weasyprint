from pathlib import Path

import django
from django.conf import settings
from django.urls import path
from django.views.generic import TemplateView

from django_weasyprint import WeasyTemplateResponseMixin, WeasyTemplateView, views


class BaseView(TemplateView):
    # simple Django CBV with template
    template_name = 'example.html'


class PDFView(WeasyTemplateResponseMixin, BaseView):
    # just add mixin and set content-type
    content_type = views.CONTENT_TYPE_PDF
    # set filename for download
    pdf_filename = 'le-foo.pdf'


class PNGView(WeasyTemplateView):
    # png view from scratch
    template_name = 'example.html'
    content_type = views.CONTENT_TYPE_PNG


urlpatterns = [
    path('html/', BaseView.as_view()),
    path('pdf/', PDFView.as_view()),
    path('png/', PNGView.as_view()),
]


settings.configure(
    ALLOWED_HOSTS=['testserver'],
    ROOT_URLCONF=__name__,
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
