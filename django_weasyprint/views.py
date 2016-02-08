from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint


class PDFTemplateResponse(TemplateResponse):
    def __init__(self, filename=None, target=None, stylesheets=None, *args, **kwargs):
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        self._target = target
        self._stylesheets = stylesheets or []
        if filename:
            self['Content-Disposition'] = 'attachment; filename="%s"' % filename

    def get_base_url(self):
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

        if self._target:
            weasy_html.write_pdf(stylesheets=weasy_css, target=self._target)
            return None

        return weasy_html.write_pdf(stylesheets=weasy_css)


class PDFTemplateResponseMixin(TemplateResponseMixin):
    response_class = PDFTemplateResponse
    filename = None
    target = None
    stylesheets = []

    def get_filename(self):
        """
        Returns the filename of the rendered PDF.
        """
        return self.filename

    def get_target(self):
        """
        Returns the target for the rendered PDF.
        """
        return self.target

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
        kwargs['target'] = self.get_target()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
