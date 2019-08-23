"""URLs for django_fido application tests."""
from django.conf.urls import url

from django_weasyprint.views import WeasyTemplateView

urlpatterns = [
    url(r'^pdf/$', WeasyTemplateView.as_view(template_name='example.html')),
]
