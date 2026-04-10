# Django-WeasyPrint

[![Build](https://github.com/fdemmer/django-weasyprint/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/fdemmer/django-weasyprint/actions?workflow=CI)
[![Coverage](https://codecov.io/github/fdemmer/django-weasyprint/branch/main/graph/badge.svg?token=aF7vd6Cx2P)](https://codecov.io/github/fdemmer/django-weasyprint)
[![PyPI Download](https://img.shields.io/pypi/v/django-weasyprint.svg)](https://pypi.python.org/pypi/django-weasyprint/)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/django-weasyprint.svg)](https://pypi.python.org/pypi/django-weasyprint/)
[![PyPI License](https://img.shields.io/pypi/l/django-weasyprint.svg)](https://pypi.python.org/pypi/django-weasyprint/)

A [Django] [WeasyPrint] integration providing class-based view and response
class for generating PDF from templates.


## Installation

Install and update using [pip]:

```
pip install -U django-weasyprint
```

[WeasyPrint] is automatically installed as a dependency of this package.
If you run into any problems be sure to check their [install instructions](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#installation) for help!

> **Tip:** In version 53 WeasyPrint switched to [pydyf] as PDF generator instead of Cairo.
> With that change PNG output was dropped and you might encounter other
> changes in the generated PDF.
>
> You can continue using WeasyPrint/Cairo by installing django-weasyprint 1.x!


## Usage

Use `WeasyTemplateView` as class based view base class or the
mixin `WeasyTemplateResponseMixin` on a `TemplateView` (or subclass
thereof).


## Example

```python
# views.py
import functools

from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin
from django_weasyprint.views import WeasyTemplateResponse
from django_weasyprint.utils import django_url_fetcher


class MyDetailView(DetailView):
    # vanilla Django DetailView
    template_name = 'mymodel.html'

def custom_url_fetcher(url, *args, **kwargs):
    # rewrite requests for CDN URLs to file path in STATIC_ROOT to use local file
    cloud_storage_url = 'https://s3.amazonaws.com/django-weasyprint/static/'
    if url.startswith(cloud_storage_url):
        url = 'file://' + url.replace(cloud_storage_url, settings.STATIC_URL)
    return django_url_fetcher(url, *args, **kwargs)

class CustomWeasyTemplateResponse(WeasyTemplateResponse):
    # customized response class to pass a kwarg to URL fetcher
    def get_url_fetcher(self):
        # disable host and certificate check
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return functools.partial(custom_url_fetcher, ssl_context=context)

class PrintView(WeasyTemplateResponseMixin, MyDetailView):
    # output of MyDetailView rendered as PDF with hardcoded CSS
    pdf_stylesheets = [
        settings.STATIC_ROOT + 'css/app.css',
    ]
    # show pdf in-line (default: True, show download dialog)
    pdf_attachment = False
    # custom response class to configure url-fetcher
    response_class = CustomWeasyTemplateResponse

class DownloadView(WeasyTemplateResponseMixin, MyDetailView):
    # suggested filename (is required for attachment/download!)
    pdf_filename = 'foo.pdf'
    # set PDF variant to 'pdf/ua-1' (see weasyprint.DEFAULT_OPTIONS)
    pdf_options = {'pdf_variant': 'pdf/ua-1'}

class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
    # dynamically generate filename
    def get_pdf_filename(self):
        return 'foo-{at}.pdf'.format(
            at=timezone.now().strftime('%Y%m%d-%H%M'),
        )

def simple_function_view(request):
    # minimal boilerplate usage :)
    return WeasyTemplateResponse(request, 'example.html', context={})
```

```python
# tasks.py
from celery import shared_task
from django.template.loader import render_to_string

from django_weasyprint.utils import django_url_fetcher

@shared_task
def generate_pdf(filename='mymodel.pdf'):
    weasy_html = weasyprint.HTML(
        string=render_to_string('mymodel.html'),
        url_fetcher=django_url_fetcher,
        base_url='file://',
    )
    weasy_html.write_pdf(filename)
```

```html
<!-- mymodel.html -->
<!doctype html>
<html>
    <head>
        <!-- Use "static" template tag and configure STATIC_URL as usual. -->
        <link rel="stylesheet" href="{% static 'css/app.css' %}" />
    </head>
    <body>
        Hello PDF-world!
    </body>
</html>
```


## Settings

By default `WeasyTemplateResponse` determines the `base_url` for
[weasyprint.HTML] and [weasyprint.CSS] automatically using Django's
`request.build_absolute_uri()`.

To disable that set `WEASYPRINT_BASEURL` to a fixed value, e.g.:

```python
# Disable prefixing relative URLs with request.build_absolute_uri().
# Instead, handle them as absolute file paths.
WEASYPRINT_BASEURL = '/'
```


## Changelog

See [CHANGELOG.md]


## Links

- Releases: https://pypi.python.org/pypi/django-weasyprint
- Issue tracker: https://github.com/fdemmer/django-weasyprint/issues
- Code: https://github.com/fdemmer/django-weasyprint


[pip]: https://pip.pypa.io/en/stable/quickstart
[Django]: https://www.djangoproject.com
[WeasyPrint]: http://weasyprint.org
[pydyf]: https://doc.courtbouillon.org/pydyf/stable/
[weasyprint.HTML]: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html?highlight=base_url#weasyprint.HTML
[weasyprint.CSS]: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html?#weasyprint.CSS
[CHANGELOG.md]: https://github.com/fdemmer/django-weasyprint/blob/main/CHANGELOG.md
