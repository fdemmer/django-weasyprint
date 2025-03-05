import weasyprint

from django.conf import settings
from django.template.response import TemplateResponse
from django.views.generic.base import ContextMixin, TemplateResponseMixin, View

from django_weasyprint.utils import django_url_fetcher


class WeasyTemplateResponse(TemplateResponse):
    def __init__(
            self,
            request,
            template,
            context=None,
            content_type=None,
            status=None,
            charset=None,
            using=None,
            headers=None,
            filename=None,
            attachment=True,
            stylesheets=None,
            options=None,
        ):
        """
        An HTTP response class with template and context rendered to a PDF document.

        Django TemplateResponse arguments:

        :param request: the request object
        :param template: template to use to render the response
        :param context: context to use to render the response
        :param content_type: content type of the response (default: 'application/pdf')
        :param status: status code of the response (default: 200)
        :param charset: character set of the response (default: settings.DEFAULT_CHARSET)
        :param using: template engine to use (default: 'django')
        :param headers: dictionary of headers to use in the response

        WeasyPrint specific arguments:

        :param filename: set `Content-Disposition` to use this filename
        :param attachment: set `Content-Disposition` 'attachment';
            A `filename` must be given to enable this even if set to `True`.
            (default: `True`)
        :param stylesheets: list of additional stylesheets
        :param options: dictionary of options passed to WeasyPrint
        """
        self._stylesheets = stylesheets or []
        self._options = options.copy() if options else {}

        kwargs = dict(
            context=context,
            content_type=content_type or WeasyTemplateResponseMixin.content_type,
            status=status,
            charset=charset,
            using=using,
            headers=headers,
        )
        super().__init__(request, template, **kwargs)

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
        Load additional stylesheets.
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

        self._options.setdefault(
            'stylesheets',
            self.get_css(base_url, url_fetcher, font_config),
        )

        return html.render(
            font_config=font_config,
            **self._options,
        )

    @property
    def rendered_content(self):
        """
        Returns rendered PDF pages.
        """
        document = self.get_document()
        return document.write_pdf(**self._options)


class WeasyTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for a CBV creating a ``WeasyTemplateResponse`` using the configured template.
    """
    response_class = WeasyTemplateResponse
    content_type = 'application/pdf'
    pdf_filename = None
    pdf_attachment = True
    pdf_stylesheets = []
    pdf_options = {}

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

    def get_pdf_options(self):
        """
        Returns dictionary of WeasyPrint options.
        """
        return self.pdf_options

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
            'options': self.get_pdf_options(),
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
