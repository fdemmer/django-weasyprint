from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin, TemplateView

import weasyprint


class PDFTemplateResponse(TemplateResponse):

    """
    absolute path of the target pdf file 
    """
    target = None

    def __init__(self, filename=None, target=None, *args, **kwargs):
        
        kwargs['content_type'] = "application/pdf"
        super(PDFTemplateResponse, self).__init__(*args, **kwargs)
        if filename:
            self['Content-Disposition'] = 'attachment; filename="%s"' % filename
        else:
            self['Content-Disposition'] = 'attachment'
            
        if target:
            self.target = target 

    @property
    def rendered_content(self):
        """Returns the rendered pdf"""
        html = super(PDFTemplateResponse, self).rendered_content
        base_url = self._request.build_absolute_uri("/")
        if self.target:
            """
            write the PDF to a file
            """
            weasyprint.HTML(string=html, base_url=base_url).write_pdf(target=self.target)
            return None
        else:
            pdf = weasyprint.HTML(string=html, base_url=base_url).write_pdf()
            return pdf


class PDFTemplateResponseMixin(TemplateResponseMixin):
    
    response_class = PDFTemplateResponse
    filename = None
    target = None


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

    def render_to_response(self, *args, **kwargs):
        """
        Returns a response, giving the filename parameter to PDFTemplateResponse.
        """
        kwargs['filename'] = self.get_filename()
        kwargs['target'] = self.get_target()
        return super(PDFTemplateResponseMixin, self).render_to_response(*args, **kwargs)


class PDFTemplateView(TemplateView, PDFTemplateResponseMixin):
    pass
