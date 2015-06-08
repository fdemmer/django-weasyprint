from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint


class PDFTemplateResponse(TemplateResponse):
    def __init__(self, filename=None, stylesheets=[], *args, **kwargs):
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        if filename:
            self['Content-Disposition'] = 'attachment; filename="%s"' % filename
        else:
            self['Content-Disposition'] = 'attachment'
        if stylesheets:
            self._stylesheets = stylesheets

    @property
    def rendered_content(self):
        """Returns the rendered pdf"""
        html = super(PDFTemplateResponse, self).rendered_content
        if hasattr(settings, 'WEASYPRINT_BASEURL'):
            base_url = settings.WEASYPRINT_BASEURL
        else:
            base_url = self._request.build_absolute_uri("/")
        if self._stylesheets:
            for index, value in enumerate(self._stylesheets):
                """
                Generate CSS objects.
                If an element is a string of css weasyprint.CSS will raise and 
                """
                try:
                    self._stylesheets[index] = weasyprint.CSS(value)
                except IOError:
                    self._stylesheets[index] = weasyprint.CSS(string=value)
                    pass
        pdf = weasyprint.HTML(string=html, base_url=base_url).write_pdf(stylesheets=self._stylesheets)
        return pdf


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
    filename = None
    stylesheets = []

    def get_filename(self):
        """
        Returns the filename of the rendered PDF.
        """
        return self.filename

    def get_stylesheets(self):
        """
        Returns the filename of the stylesheet to use when rendering.
        """
        return self.stylesheets

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response, giving the filename parameter to PDFTemplateResponse.
        """
        kwargs['filename'] = self.get_filename()
        kwargs['stylesheets'] = self.get_stylesheets()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
