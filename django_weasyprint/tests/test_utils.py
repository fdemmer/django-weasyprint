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

    def assert_data(self, data, filename, mime_type):
        self.assertEqual(
            sorted(data.keys()),
            ['encoding', 'file_obj', 'filename', 'mime_type'],
        )
        self.assertEqual(data['filename'], filename)
        self.assertEqual(data['mime_type'], mime_type)
        self.assertEqual(data['encoding'], None)

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT='/www/media')
    @mock.patch('django_weasyprint.utils.default_storage.open')
    @mock.patch('weasyprint.default_url_fetcher')
    def test_media(self, mock_fetcher, mock_open):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        data = django_url_fetcher(url)
        mock_fetcher.assert_not_called()
        mock_open.assert_called_once_with('/www/media/image.jpg', 'rb')
        self.assert_data(data, 'image.jpg', 'image/jpeg')

    @override_settings(MEDIA_URL='/media/', MEDIA_ROOT=Path('/www/media'))
    @mock.patch('django_weasyprint.utils.default_storage.open')
    @mock.patch('weasyprint.default_url_fetcher')
    def test_media_root_pathlib(self, mock_fetcher, mock_open):
        # request matches MEDIA_URL, request handled
        url = 'file:///media/image.jpg'
        data = django_url_fetcher(url)
        mock_fetcher.assert_not_called()
        mock_open.assert_called_once_with('/www/media/image.jpg', 'rb')
        self.assert_data(data, 'image.jpg', 'image/jpeg')

    @override_settings(STATIC_URL='/static/', STATIC_ROOT='/www/static')
    @mock.patch('django_weasyprint.utils.open')
    @mock.patch('django_weasyprint.utils.find', return_value='/www/static/css/styles.css')
    @mock.patch('weasyprint.default_url_fetcher')
    def test_static(self, mock_fetcher, mock_find, mock_open):
        # request matches STATIC_URL, request handled
        url = 'file:///static/css/styles.css'
        data = django_url_fetcher(url)
        mock_fetcher.assert_not_called()
        mock_find.assert_called_once_with('css/styles.css')
        mock_open.assert_called_once_with('/www/static/css/styles.css', 'rb')
        self.assert_data(data, 'styles.css', 'text/css')

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
    @mock.patch('weasyprint.default_url_fetcher')
    def test_manifest_static(self, mock_fetcher, mock_find, mock_open, mock_reverse):
        # request matches STATIC_URL, request handled
        url = 'file:///static/css/styles.60b250d16a6a.css'
        data = django_url_fetcher(url)
        mock_fetcher.assert_not_called()
        mock_find.assert_called_once_with('css/styles.css')
        mock_open.assert_called_once_with('/www/static/css/styles.css', 'rb')
        self.assert_data(data, 'styles.css', 'text/css')

    @override_settings(STATIC_URL='/static/', STATIC_ROOT='/www/static')
    @mock.patch('django_weasyprint.utils.open')
    @mock.patch('django_weasyprint.utils.find', return_value=None)
    @mock.patch('weasyprint.default_url_fetcher')
    def test_static_file_not_found(self, mock_fetcher, mock_find, mock_open):
        # request matches STATIC_URL, request handled, but staticfiles finder returns None
        url = 'file:///static/css/missing.css'
        django_url_fetcher(url)
        mock_find.assert_called_once_with('css/missing.css')
        mock_open.assert_not_called()
        # request was forwarded to default fetcher
        mock_fetcher.assert_called_once_with('file:///static/css/missing.css')
