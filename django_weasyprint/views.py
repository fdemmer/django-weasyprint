# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint


CONTENT_TYPE_PNG = 'image/png'
CONTENT_TYPE_PDF = 'application/pdf'


class WeasyTemplateResponse(TemplateResponse):

    def __init__(self, filename=None, stylesheets=None, *args, **kwargs):
        """

        :param filename:
        :param stylesheets:
        """
        self._stylesheets = stylesheets or []
        self._content_type = kwargs.get('content_type')
        super(WeasyTemplateResponse, self).__init__(*args, **kwargs)
        if filename:
            self['Content-Disposition'] = 'attachment; %s' % filename

    def get_base_url(self):
        """
        Determine base URL to fetch CSS files from. First one defined is used:

            - `settings.WEASYPRINT_BASEURL`
            - `settings.STATIC_URL`
            - root path of the URL used in the request.

        :return:
        """
        for attr in ['WEASYPRINT_BASEURL', 'STATIC_URL']:
            try:
                return getattr(settings, attr)
            except AttributeError:
                pass
        return self._request.build_absolute_uri('/')

    def get_css(self, base_url):
        tmp = []
        for value in self._stylesheets:
            #TODO test with missing or invalid css
            css = weasyprint.CSS(value, base_url=base_url)
            if css:
                tmp.append(css)
        return tmp

    def get_document(self):
        """
        Returns a :class:`~document.Document` object which provides
        access to individual pages and various meta-data.

        See :meth:`weasyprint.HTML.render` and
        :meth:`weasyprint.document.Document.write_pdf` on how to generate a
        PDF file.
        """
        base_url = self.get_base_url()
        content = super(WeasyTemplateResponse, self).rendered_content

        html = weasyprint.HTML(string=content, base_url=base_url)
        return html.render(self.get_css(base_url))

    @property
    def rendered_content(self):
        """
        Returns rendered PDF pages.
        """
        document = self.get_document()
        if CONTENT_TYPE_PNG in self._content_type:
            return document.write_png()
        return document.write_pdf()


class WeasyTemplateResponseMixin(TemplateResponseMixin):
    response_class = WeasyTemplateResponse
    content_type = CONTENT_TYPE_PDF
    pdf_filename = None
    pdf_stylesheets = []

    def get_pdf_filename(self):
        """
        Returns :attr:`pdf_filename` value by default.

        If left blank the browser will display the PDF inline.
        Otherwise it will pop up the "Save as.." dialog.

        :rtype: :func:`str`
        """
        return self.pdf_filename

    def get_pdf_stylesheets(self):
        """
        Returns a list of stylesheet filenames to use when rendering.

        :rtype: :func:`list`
        """
        return self.pdf_stylesheets

    def render_to_response(self, context, **response_kwargs):
        """
        Renders PDF document and prepares response by calling on
        :attr:`response_class` (default: :class:`WeasyTemplateResponse`).

        :returns: Django HTTP response
        :rtype: :class:`django.http.HttpResponse`
        """
        response_kwargs.update({
            'filename': self.get_pdf_filename(),
            'stylesheets': self.get_pdf_stylesheets(),
        })
        return super(WeasyTemplateResponseMixin, self).render_to_response(
            context, **response_kwargs
        )


class WeasyTemplateView(TemplateView, WeasyTemplateResponseMixin):
    """
    Concrete view for serving PDF files.

    .. code-block:: python

        class HelloPDFView(WeasyTemplateView):
            template_name = "hello.html"
    """
    pass
