from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase, override_settings

import django_weasyprint.tests  # noqa
from django_weasyprint.utils import django_url_fetcher


class URLFetcherTest(SimpleTestCase):
    def test_default(self):
        # MEDIA_URL='' and STATIC_URL=None, all requests passed though
        url = 'http://s3.amazon.test/images/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            django_url_fetcher(url)
        url_fetcher.assert_called_once_with(url)

        url = 'file:///media/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            django_url_fetcher(url)
        url_fetcher.assert_called_once_with(url)

        url = 'file:///static/styles.css'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            django_url_fetcher(url)
        url_fetcher.assert_called_once_with(url)

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT='/media')
    @mock.patch('django_weasyprint.utils.default_storage')
    def test_media(self, mock_storage):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'image.jpg')
        self.assertEqual(data['mime_type'], 'image/jpeg')
        self.assertEqual(data['encoding'], None)

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT=Path('/media'))
    @mock.patch('django_weasyprint.utils.default_storage')
    def test_media_root_pathlib(self, mock_storage):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'image.jpg')
        self.assertEqual(data['mime_type'], 'image/jpeg')
        self.assertEqual(data['encoding'], None)

    @override_settings(STATIC_URL='/static/', STATIC_ROOT='/static')
    @mock.patch('django_weasyprint.utils.open')
    def test_static(self, mock_open):
        # request matches STATIC_URL, request handled
        url = 'file:///static/styles.css'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'styles.css')
        self.assertEqual(data['mime_type'], 'text/css')
        self.assertEqual(data['encoding'], None)
