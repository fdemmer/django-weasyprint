django-weasyprint
=================

A `Django`_ class-based view generating PDF responses using `WeasyPrint`_.

Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U django-weasyprint

Usage
-----

Use ``WeasyTemplateView`` as class based view base class or the just the
mixin ``WeasyTemplateResponseMixin`` on a ``TemplateView`` (or subclass
thereof).

Example
-------

.. code:: python

    from django.conf import settings
    from django.views.generic import DetailView

    from django_weasyprint import CONTENT_TYPE_PNG, WeasyTemplateResponseMixin


    class MyModelView(DetailView):
        # vanilla Django DetailView
        model = MyModel
        template_name = 'mymodel.html'


    class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
        # output of DetailView rendered as PDF
        pdf_stylesheets = [
            settings.STATIC_ROOT + 'css/app.css',
        ]


    class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
        # generate a PNG image instead
        content_type = CONTENT_TYPE_PNG


Links
-----

* Releases: https://pypi.python.org/pypi/django-weasyprint
* Issue tracker: https://github.com/fdemmer/django-weasyprint/issues
* Code: https://github.com/fdemmer/django-weasyprint


.. _pip: https://pip.pypa.io/en/stable/quickstart
.. _Django: https://www.djangoproject.com
.. _WeasyPrint: http://weasyprint.org
