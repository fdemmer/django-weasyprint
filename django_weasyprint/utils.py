# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import mimetypes
from urllib import parse

from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.core.files.storage import default_storage
from os.path import basename

import weasyprint


def django_url_fetcher(url):
    # load file:// paths directly from disk
    if url.startswith('file:'):
        mime_type, encoding = mimetypes.guess_type(url)
        url_path = parse.urlparse(url).path
        data = {
            'mime_type': mime_type,
            'encoding': encoding,
            'filename': basename(url_path),
        }

        if url_path.startswith(settings.MEDIA_URL):
            path = url_path.replace(settings.MEDIA_URL, settings.MEDIA_ROOT)
            data['file_obj'] = default_storage.open(path)
            return data

        elif url_path.startswith(settings.STATIC_URL):
            path = url_path.replace(settings.STATIC_URL, '')
            data['file_obj'] = open(find(path), 'rb')
            return data

    # fall back to weasyprint default fetcher
    return weasyprint.default_url_fetcher(url)
