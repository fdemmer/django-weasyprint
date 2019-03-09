from django.urls import path
from django_weasyprint.tests.testproject.testapp import views


urlpatterns = [
    path('sample1.pdf', views.Sample1View.as_view(), name='sample1'),
]
