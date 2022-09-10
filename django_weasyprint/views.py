import weasyprint
from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View

from django_weasyprint.utils import django_url_fetcher


class WeasyTemplateResponse(TemplateResponse):
    def __init__(self, filename=None, stylesheets=None, attachment=True,
                 *args, **kwargs):
        """
        An HTTP response class with PDF or PNG document as content.

        :param filename: set `Content-Disposition` to use this filename
        :param attachment: set `Content-Disposition` 'attachment', a `filename`
            must be given if `True` (default: `True`)
        :param stylesheets: list of additional stylesheets
        """
        self._stylesheets = stylesheets or []
        super().__init__(*args, **kwargs)
        if filename:
            display = 'attachment' if attachment else 'inline'
            self['Content-Disposition'] = f'{display};filename="{filename}"'

    def get_base_url(self):
        """
        Determine base URL to fetch CSS or other files referenced with relative
        paths in the HTML files using the `WEASYPRINT_BASEURL` setting or
        fall back to using the root path of the URL used in the request.
        """
        return getattr(
            settings, 'WEASYPRINT_BASEURL',
            self._request.build_absolute_uri('/')
        )

    def get_url_fetcher(self):
        """
        Determine the URL fetcher to fetch CSS, images, fonts, etc. from.
        """
        return django_url_fetcher

    def get_font_config(self):
        """
        A FreeType font configuration to handle @font-config rules.
        """
        return weasyprint.text.fonts.FontConfiguration()

    def get_css(self, base_url, url_fetcher, font_config):
        """
        Load addtional additional stylesheets.
        """
        return [
            weasyprint.CSS(
                value,
                base_url=base_url,
                url_fetcher=url_fetcher,
                font_config=font_config,
            )
            for value
            in self._stylesheets
        ]

    def get_document(self):
        """
        Returns a :class:`~document.Document` object which provides
        access to individual pages and various meta-data.

        See :meth:`weasyprint.HTML.render` and
        :meth:`weasyprint.document.Document.write_pdf` on how to generate a
        PDF file.
        """
        base_url = self.get_base_url()
        url_fetcher = self.get_url_fetcher()
        font_config = self.get_font_config()

        html = weasyprint.HTML(
            string=super().rendered_content,
            base_url=base_url,
            url_fetcher=url_fetcher,
        )
        return html.render(
            self.get_css(base_url, url_fetcher, font_config),
            font_config=font_config,
        )

    @property
    def rendered_content(self):
        """
        Returns rendered PDF pages.
        """
        document = self.get_document()
        return document.write_pdf()


class WeasyTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for a CBV creating a ``WeasyTemplateResponse`` using the configured template.
    """
    response_class = WeasyTemplateResponse
    content_type = 'application/pdf'
    pdf_filename = None
    pdf_attachment = True
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
            'attachment': self.pdf_attachment,
            'filename': self.get_pdf_filename(),
            'stylesheets': self.get_pdf_stylesheets(),
        })
        return super().render_to_response(
            context, **response_kwargs
        )


class WeasyTemplateView(WeasyTemplateResponseMixin, ContextMixin, View):
    """
    Concrete view for serving PDF files.

    .. code-block:: python

        class HelloPDFView(WeasyTemplateView):
            template_name = "hello.html"
    """
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
