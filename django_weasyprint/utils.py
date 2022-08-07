import logging
import mimetypes
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse

import weasyprint
from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage
from django.urls import get_script_prefix

log = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_reversed_hashed_files():
    return {v: k for k, v in staticfiles_storage.hashed_files.items()}


def django_url_fetcher(url, *args, **kwargs):
    # attempt to load file:// paths to Django MEDIA or STATIC files directly from disk
    if url.startswith('file:'):
        log.debug('Attempt to fetch from %s', url)
        mime_type, encoding = mimetypes.guess_type(url)
        url_path = urlparse(url).path
        data = {
            'mime_type': mime_type,
            'encoding': encoding,
            'filename': Path(url_path).name,
        }

        default_media_url = settings.MEDIA_URL in ('', get_script_prefix())
        if not default_media_url and url_path.startswith(settings.MEDIA_URL):
            log.debug('URL contains MEDIA_URL (%s)', settings.MEDIA_URL)
            cleaned_media_root = str(settings.MEDIA_ROOT)
            if not cleaned_media_root.endswith('/'):
                cleaned_media_root += '/'
            path = url_path.replace(settings.MEDIA_URL, cleaned_media_root, 1)
            log.debug('Cleaned path: %s', path)
            data['file_obj'] = default_storage.open(path, 'rb')
            return data

        # path looks like a static file based on configured STATIC_URL
        elif settings.STATIC_URL and url_path.startswith(settings.STATIC_URL):
            log.debug('URL contains STATIC_URL (%s)', settings.STATIC_URL)
            # strip the STATIC_URL prefix to get the relative filesystem path
            relative_path = url_path.replace(settings.STATIC_URL, '', 1)
            # detect hashed files storage and get path with un-hashed filename
            if hasattr(staticfiles_storage, 'hashed_files'):
                log.debug('Hashed static files storage detected')
                relative_path = get_reversed_hashed_files()[relative_path]
                data['filename'] = Path(relative_path).name
            log.debug('Cleaned path: %s', relative_path)
            # find the absolute path using the static file finders
            absolute_path = find(relative_path)
            log.debug('Static file finder returned: %s', absolute_path)
            if absolute_path:
                log.debug('Loading static file: %s', absolute_path)
                data['file_obj'] = open(absolute_path, 'rb')
                return data

    # Fall back to weasyprint default fetcher for http/s: and file: paths
    # that did not match MEDIA_URL or STATIC_URL.
    log.debug('Forwarding to weasyprint.default_url_fetcher: %s', url)
    return weasyprint.default_url_fetcher(url, *args, **kwargs)
