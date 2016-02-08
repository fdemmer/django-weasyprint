# django-weasyprint

A class-based view that generated pdfs using WeasyPrint

## About this fork

I combined all the forks lying around.

Then I found out weasyprint does not support 'rem' units. :(
So I stopped working on it.

## Usage

Use `PDFTemplateView` as class based view base class or the just the mixin 
`PDFTemplateResponseMixin` on a `TemplateView` (or subclass thereof).

## Example

```python
from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import PDFTemplateResponseMixin


class MyModelView(DetailView):
    model = MyModel
    template_name = 'mymodel.html'


class MyModelViewPrintView(PDFTemplateResponseMixin, MyModelView):
    stylesheets = [
        settings.STATIC_ROOT + "css/app.css",
    ]
```
