from django.conf.urls import url, include
from django_weasyprint.tests.testproject.testapp import urls

urlpatterns = [
    url(r'^', include(urls)),
]
