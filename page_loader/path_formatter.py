#!/usr/bin/env python3

"""Path formatter."""

import re
from urllib.parse import urlparse


def path_formatter(url, output):
    parsed_url = urlparse(url)
    hostname = change_symbols(parsed_url.netloc)
    path = change_symbols(parsed_url.path)
    return {
        'original_url': url,
        'host_name': change_symbols(parsed_url.netloc),
        'path_to_html': '{0}/{1}{2}.html'.format(output, hostname, path),
        'path_to_files': '{0}/{1}{2}_files'.format(output, hostname, path),
    }


def path_to_file(src, path_builder):
    return '{0}/{1}{2}'.format(
        path_builder['path_to_files'],
        path_builder['host_name'],
        change_symbols(src),
    )


def change_symbols(path):
    path_with_dashes = re.sub(r'[^A-Za-z\d]', '-', path)
    return re.sub('-(?=jpg|png)', '.', path_with_dashes)
