# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint


class PDFTemplateResponse(TemplateResponse):
    def __init__(self, filename=None, target=None, stylesheets=None, *args, **kwargs):
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        self._stylesheets = stylesheets or []
        if filename:
            self['Content-Disposition'] = 'attachment; %s' % filename

    def get_base_url(self):
        """
        Determine base URL to fetch CSS files from `WEASYPRINT_BASEURL` or
        fall back to using the root path of the URL used in the request.

        :return:
        """
        return getattr(
            settings, 'WEASYPRINT_BASEURL',
            self._request.build_absolute_uri('/')
        )

    def get_css(self, base_url):
        tmp = []
        for value in self._stylesheets:
            try:
                css = weasyprint.CSS(value, base_url=base_url)
            except IOError:
                css = weasyprint.CSS(string=value, base_url=base_url)
            if css:
                tmp.append(css)
        return tmp

    @property
    def rendered_content(self):
        """Returns the rendered pdf"""
        html = super(PDFTemplateResponse, self).rendered_content
        base_url = self.get_base_url()

        weasy_html = weasyprint.HTML(string=html, base_url=base_url)
        weasy_css = self.get_css(base_url)


        return weasy_html.write_pdf(stylesheets=weasy_css)


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
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
        :attr:`response_class` (default: :class:`PDFTemplateResponse`).

        :returns: Django HTTP response
        :rtype: :class:`django.http.HttpResponse`
        """
        response_kwargs.update({
            'filename': self.get_pdf_filename(),
            'stylesheets': self.get_pdf_stylesheets(),
        })
        return super(PDFTemplateResponseMixin, self).render_to_response(
            context, **response_kwargs
        )


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    """
    Concrete view for serving PDF files.

    .. code-block:: python

        class HelloPDFView(PDFTemplateView):
            template_name = "hello.html"
    """
    pass
