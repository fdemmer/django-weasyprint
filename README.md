# django-weasyprint

A class-based view that generated PDFs using WeasyPrint

## Usage

Use `WeasyTemplateView` as class based view base class or the just the mixin 
`WeasyTemplateResponseMixin` on a `TemplateView` (or subclass thereof).

## Example

```python
from django.conf import settings
from django.views.generic import DetailView

from django_weasyprint import WeasyTemplateResponseMixin


class MyModelView(DetailView):
    model = MyModel
    template_name = 'mymodel.html'


class MyModelViewPrintView(WeasyTemplateResponseMixin, MyModelView):
    stylesheets = [
        settings.STATIC_ROOT + "css/app.css",
    ]
```
## History

2016-02-08: forked to merge open pull requests

2017-01-13: official repository taken over from https://github.com/dekkers/
