django-weasyprint
=================

A Django class-based view generating PDF resposes using WeasyPrint.

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

    from django_weasyprint import WeasyTemplateResponseMixin


    class MyModelView(DetailView):
        model = MyModel
        template_name = 'mymodel.html'


    class MyModelViewPrintView(WeasyTemplateResponseMixin, MyModelView):
        pdf_stylesheets = [
            settings.STATIC_ROOT + "css/app.css",
        ]

History
-------

2017-02-02: finally pushed new release to pypi

2016-02-08: forked to merge open pull requests

2016-01-13: official repository taken over from https://github.com/dekkers/
