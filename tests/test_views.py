from importlib.metadata import version
from unittest import mock

from packaging.version import Version

from django.test import SimpleTestCase


class WeasyTemplateViewTestCase(SimpleTestCase):
    def test_get_html(self):
        response = self.client.get('/html/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(response.has_header('content-type'))
        self.assertEqual(response['content-type'], 'text/html; charset=utf-8')
        self.assertEqual(response.content, b'<h1>Example template</h1>\n')

    # why lambda? why not just new?
    # https://stackoverflow.com/q/55197479/652457
    @mock.patch('weasyprint.open', new_callable=lambda: mock.mock_open(read_data=b''))
    @mock.patch('weasyprint.urls.open', new_callable=lambda: mock.mock_open(read_data=b''))  # noqa: E501
    def test_get_pdf_download_and_options(self, mock_open, mock_open_old):
        response = self.client.get('/pdf/download/')
        self.assertEqual(response.status_code, 200)

        if Version(version('weasyprint')) < Version('68'):
            mock_open = mock_open_old

        # additional css from pdf_stylesheets attribute
        mock_open.assert_called_once_with('/static/css/print.css', 'rb')

        self.assertTrue(response.has_header('content-type'))
        self.assertEqual(response['content-type'], 'application/pdf')
        self.assertTrue(response.has_header('content-disposition'))
        self.assertEqual(
            response['content-disposition'],
            'attachment;filename="le-foo.pdf"',
        )
        self.assertEqual(response.content[:8], b'%PDF-1.6')

    def test_get_pdf(self):
        urls = [
            '/pdf/',
            '/pdf/view/',
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

                self.assertTrue(response.has_header('content-type'))
                self.assertEqual(response['content-type'], 'application/pdf')
                self.assertFalse(response.has_header('content-disposition'))
                self.assertEqual(response.content[:4], b'%PDF')
