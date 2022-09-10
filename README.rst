django-weasyprint
=================

|Build| |Coverage| |PyPI Download| |PyPI Python Versions| |PyPI License|

.. |Build| image:: https://github.com/fdemmer/django-weasyprint/workflows/CI/badge.svg?branch=main
    :target: https://github.com/fdemmer/django-weasyprint/actions?workflow=CI

.. |Coverage| image:: https://codecov.io/gh/fdemmer/django-weasyprint/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/fdemmer/django-weasyprint

.. |PyPI Download| image:: https://img.shields.io/pypi/v/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/

.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/

.. |PyPI License| image:: https://img.shields.io/pypi/l/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/


A `Django`_ class-based view generating PDF responses using `WeasyPrint`_.


Installation
------------

Install and update using `pip`_:

.. code-block:: text

    pip install -U django-weasyprint

`WeasyPrint`_ is automatically installed as a dependency of this package.
If you run into any problems be sure to check their `install instructions
<https://weasyprint.readthedocs.io/en/latest/install.html>`_ for help!

.. tip::

   In version 53 WeasyPrint switched to `pydyf`_ as PDF generator instead of Cairo.
   With that change PNG output was dropped and you might encounter other
   changes in the generated PDF.

   You can continue using WeasyPrint/Cairo by installing django-weasyprint 1.x!


Usage
-----

Use ``WeasyTemplateView`` as class based view base class or the just the
mixin ``WeasyTemplateResponseMixin`` on a ``TemplateView`` (or subclass
thereof).


Example
-------

.. code:: python

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

    class DynamicNameView(WeasyTemplateResponseMixin, MyDetailView):
        # dynamically generate filename
        def get_pdf_filename(self):
            return 'foo-{at}.pdf'.format(
                at=timezone.now().strftime('%Y%m%d-%H%M'),
            )

.. code:: html

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


Settings
--------

By default ``WeasyTemplateResponse`` determines the ``base_url`` for
`weasyprint.HTML`_ and `weasyprint.CSS`_ automatically using the request path.

To disable that set ``WEASYPRINT_BASEURL`` to a fixed value, e.g.:

.. code:: python

    # Disable prefixing relative URLs with request.path, handle as absolute file paths
    WEASYPRINT_BASEURL = '/'


Changelog
---------

See `CHANGELOG.md`_


Links
-----

* Releases: https://pypi.python.org/pypi/django-weasyprint
* Issue tracker: https://github.com/fdemmer/django-weasyprint/issues
* Code: https://github.com/fdemmer/django-weasyprint


.. _pip: https://pip.pypa.io/en/stable/quickstart
.. _Django: https://www.djangoproject.com
.. _WeasyPrint: http://weasyprint.org
.. _pydyf: https://doc.courtbouillon.org/pydyf/stable/

.. _weasyprint.HTML: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html?highlight=base_url#weasyprint.HTML
.. _weasyprint.CSS: https://doc.courtbouillon.org/weasyprint/stable/api_reference.html?#weasyprint.CSS

.. _CHANGELOG.md: https://github.com/fdemmer/django-weasyprint/blob/main/CHANGELOG.md
