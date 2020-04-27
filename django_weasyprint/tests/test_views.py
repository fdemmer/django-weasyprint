from django.test import SimpleTestCase

import django_weasyprint.tests  # noqa
from django_weasyprint.views import CONTENT_TYPE_PDF, CONTENT_TYPE_PNG


class WeasyTemplateViewTestCase(SimpleTestCase):
    def test_get_html(self):
        response = self.client.get('/html/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(sorted(response._headers.keys()), ['content-type'])
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertEqual(response.content, b'<h1>Example template</h1>\n')

    def test_get_pdf(self):
        response = self.client.get('/pdf/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            sorted(response._headers.keys()),
            ['content-disposition', 'content-type'],
        )
        self.assertEqual(response['content-type'], CONTENT_TYPE_PDF)
        self.assertEqual(
            response['content-disposition'],
            'attachment;filename="le-foo.pdf"',
        )
        self.assertEqual(response.content[:4], b'%PDF')

    def test_get_png(self):
        response = self.client.get('/png/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(sorted(response._headers.keys()), ['content-type'])
        self.assertEqual(response['content-type'], CONTENT_TYPE_PNG)
        self.assertEqual(response.content[1:4], b'PNG')
