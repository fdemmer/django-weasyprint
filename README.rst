django-weasyprint
=================

A `Django`_ class-based view generating PDF responses using `WeasyPrint`_.

|TravisCI Build| |PyPI Download| |PyPI Python Versions| |PyPI License|

.. |PyPI Download| image:: https://img.shields.io/pypi/v/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/

.. |PyPI Python Versions| image:: https://img.shields.io/pypi/pyversions/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/

.. |PyPI License| image:: https://img.shields.io/pypi/l/django-weasyprint.svg
   :target: https://pypi.python.org/pypi/django-weasyprint/

.. |TravisCI Build| image:: https://travis-ci.org/fdemmer/django-weasyprint.svg?branch=master
    :target: https://travis-ci.org/fdemmer/django-weasyprint


Installing
----------

Install and update using `pip`_:

.. code-block:: text

    pip install -U django-weasyprint

`WeasyPrint`_ is automatically installed as a dependency of this package.
If you run into any problems be sure to check their `install instructions
<https://weasyprint.readthedocs.io/en/latest/install.html>`_ for help!


Usage
-----

Use ``WeasyTemplateView`` as class based view base class or the just the
mixin ``WeasyTemplateResponseMixin`` on a ``TemplateView`` (or subclass
thereof).


Example
-------

.. code:: python

    import functools

    from django.conf import settings
    from django.views.generic import DetailView

    from django_weasyprint import WeasyTemplateResponseMixin
    from django_weasyprint.views import CONTENT_TYPE_PNG


    class MyModelView(DetailView):
        # vanilla Django DetailView
        model = MyModel
        template_name = 'mymodel.html'

    class CustomWeasyTemplateResponse(WeasyTemplateResponse):
        # customized response class to change the default URL fetcher
        def get_url_fetcher(self):
            # disable host and certificate check
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            return functools.partial(django_url_fetcher, ssl_context=context)

    class MyModelPrintView(WeasyTemplateResponseMixin, MyModelView):
        # output of MyModelView rendered as PDF with hardcoded CSS
        pdf_stylesheets = [
            settings.STATIC_ROOT + 'css/app.css',
        ]
        # show pdf in-line (default: True, show download dialog)
        pdf_attachment = False
        # custom response class to configure url-fetcher
        response_class = CustomWeasyTemplateResponse

    class MyModelDownloadView(WeasyTemplateResponseMixin, MyModelView):
        # suggested filename (is required for attachment/download!)
        pdf_filename = 'foo.pdf'

    class MyModelImageView(WeasyTemplateResponseMixin, MyModelView):
        # generate a PNG image instead
        content_type = CONTENT_TYPE_PNG

        # dynamically generate filename
        def get_pdf_filename(self):
            return 'foo-{at}.pdf'.format(
                at=timezone.now().strftime('%Y%m%d-%H%M'),
            )


Self-Signed SSL For Server Side Requests
---------

.. code-block:: sh

    # if you have not yet created a certificate
    sudo openssl req -x509 \
        -sha256 \
        -nodes \
        -newkey rsa:4096 \
        -days 365 \
        -keyout localhost.key \
        -out localhost.crt

    # follow the prompts about your certificate and the domain name

    openssl x509 -text -noout -in localhost.crt

Add your certificate to nginx.conf

.. code-block:: sh

    # include in your nginx.conf
    ssl_certificate /etc/ssl/certs/localhost.crt;
    ssl_certificate_key /etc/ssl/private/localhost.key;

Copy, and update your trusted certificates

.. code-block:: sh

    # copy new certificates

    sudo cp /etc/ssl/certs/localhost.crt /usr/local/share/ca-certificates/localhost.crt
    sudo cp /etc/ssl/private/localhost.key /usr/local/share/ca-certificates/localhost.key

    # update the certificate authority trusted certificates
    sudo update-ca-certificates

    # export your newly updated Certificate Authority Bundle file
    # if using django, it will use the newly signed certificate authority as valid
    # images will load properly
    sudo tee -a /etc/environment <<< 'export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt'

    # reboot optional
    reboot



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

.. _CHANGELOG.md: https://github.com/fdemmer/django-weasyprint/blob/master/CHANGELOG.md
