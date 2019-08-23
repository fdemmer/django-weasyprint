import os

from django.test import SimpleTestCase, override_settings

from django_weasyprint.views import CONTENT_TYPE_PDF

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    },
]


@override_settings(TEMPLATES=TEMPLATES, ROOT_URLCONF='django_weasyprint.tests.urls')
class TestWeasyTemplateView(SimpleTestCase):

    def test_get(self):
        response = self.client.get('/pdf/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], CONTENT_TYPE_PDF)
