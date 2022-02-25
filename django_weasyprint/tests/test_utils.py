from pathlib import Path
from unittest import mock

from django.test import SimpleTestCase, override_settings

import django_weasyprint.tests  # noqa
from django_weasyprint.utils import django_url_fetcher


class URLFetcherTest(SimpleTestCase):
    def test_default(self):
        # MEDIA_URL='' and STATIC_URL=None, all requests passed though
        url = 'https://s3.amazon.test/images/image.jpg'
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

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT='/www/media')
    @mock.patch('django_weasyprint.utils.default_storage.open')
    def test_media(self, mock_open):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()
        mock_open.assert_called_once_with('/www/media/image.jpg', 'rb')

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'image.jpg')
        self.assertEqual(data['mime_type'], 'image/jpeg')
        self.assertEqual(data['encoding'], None)

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT=Path('/www/media'))
    @mock.patch('django_weasyprint.utils.default_storage.open')
    def test_media_root_pathlib(self, mock_open):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()
        mock_open.assert_called_once_with('/www/media/image.jpg', 'rb')

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'image.jpg')
        self.assertEqual(data['mime_type'], 'image/jpeg')
        self.assertEqual(data['encoding'], None)

    @override_settings(STATIC_URL='/static/', STATIC_ROOT='/www/static')
    @mock.patch('django_weasyprint.utils.open')
    @mock.patch('django_weasyprint.utils.find', return_value='/www/static/css/styles.css')
    def test_static(self, mock_find, mock_open):
        # request matches STATIC_URL, request handled
        url = 'file:///static/css/styles.css'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()
        mock_find.assert_called_once_with('css/styles.css')
        mock_open.assert_called_once_with('/www/static/css/styles.css', 'rb')

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'styles.css')
        self.assertEqual(data['mime_type'], 'text/css')
        self.assertEqual(data['encoding'], None)

    @override_settings(
        STATIC_URL='/static/',
        STATIC_ROOT='/www/static',
        STATICFILES_STORAGE='django.contrib.staticfiles.storage.ManifestStaticFilesStorage',  # noqa
    )
    @mock.patch(
        'django_weasyprint.utils.get_reversed_hashed_files',
        return_value={'css/styles.60b250d16a6a.css': 'css/styles.css'}
    )
    @mock.patch('django_weasyprint.utils.open')
    @mock.patch('django_weasyprint.utils.find', return_value='/www/static/css/styles.css')
    def test_manifest_static(self, mock_find, mock_open, mock_reverse):
        # request matches STATIC_URL, request handled
        url = 'file:///static/css/styles.60b250d16a6a.css'
        with mock.patch('weasyprint.default_url_fetcher') as url_fetcher:
            data = django_url_fetcher(url)
        url_fetcher.assert_not_called()
        mock_find.assert_called_once_with('css/styles.css')
        mock_open.assert_called_once_with('/www/static/css/styles.css', 'rb')

        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], 'styles.css')
        self.assertEqual(data['mime_type'], 'text/css')
        self.assertEqual(data['encoding'], None)
