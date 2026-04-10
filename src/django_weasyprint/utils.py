import logging
import mimetypes
from functools import lru_cache
from urllib.parse import urlparse

from weasyprint.urls import URLFetcher, URLFetcherResponse

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage
from django.urls import get_script_prefix


log = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_reversed_hashed_files():
    return {v: k for k, v in staticfiles_storage.hashed_files.items()}


def guess_content_type(url, default='application/octet-stream'):
    mime_type, encoding = mimetypes.guess_type(url)
    content_type = mime_type or default
    if encoding:
        return f'{content_type};charset={encoding}'
    return content_type


class DjangoURLFetcher(URLFetcher):
    """
    Fetcher of external resources such as images or stylesheets,
    that serves Django MEDIA and STATIC files directly from disk, bypassing HTTP.
    """
    def fetch(self, url, headers=None):
        # attempt to load file:// paths to Django MEDIA or STATIC files directly from disk
        if url.startswith('file:'):
            log.debug('Attempt to fetch from %s', url)

            MEDIA_URL = settings.MEDIA_URL
            STATIC_URL = settings.STATIC_URL

            content_type = guess_content_type(url)

            url_path = urlparse(url).path

            default_media_url = MEDIA_URL in ('', get_script_prefix())
            if not default_media_url and url_path.startswith(MEDIA_URL):
                log.debug('URL contains MEDIA_URL (%s)', MEDIA_URL)

                cleaned_media_root = str(settings.MEDIA_ROOT)
                if not cleaned_media_root.endswith('/'):
                    cleaned_media_root += '/'
                absolute_path = url_path.replace(MEDIA_URL, cleaned_media_root, 1)

                log.debug('Loading media file: %s', absolute_path)
                return URLFetcherResponse(
                    url='file://' + absolute_path,
                    body=default_storage.open(absolute_path, 'rb'),
                    headers={'Content-Type': content_type},
                )

            # path looks like a static file based on configured STATIC_URL
            elif STATIC_URL and url_path.startswith(STATIC_URL):
                log.debug('URL contains STATIC_URL (%s)', STATIC_URL)

                # strip the STATIC_URL prefix to get the relative filesystem path
                relative_path = url_path.replace(STATIC_URL, '', 1)
                # detect hashed files storage and get path with un-hashed filename
                if not settings.DEBUG and hasattr(staticfiles_storage, 'hashed_files'):
                    log.debug('Hashed static files storage detected')
                    relative_path = get_reversed_hashed_files()[relative_path]
                log.debug('Cleaned path: %s', relative_path)

                # find the absolute path using the static file finders
                if absolute_path := find(relative_path):
                    log.debug('Loading static file: %s', absolute_path)
                    return URLFetcherResponse(
                        url='file://' + absolute_path,
                        body=open(absolute_path, 'rb'),  # noqa: PTH123,
                        headers={'Content-Type': content_type},
                    )

        # URLFetcher for http/s: and file: paths that do not match MEDIA_URL or STATIC_URL
        log.debug('Forwarding to URLFetcher: %s', url)
        return super().fetch(url, headers)
