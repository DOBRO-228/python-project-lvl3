#!/usr/bin/env python3

"""Path formatter."""

import os
import re
from urllib.parse import urlparse


def path_formatter(url, output):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.netloc
    path = change_symbols(parsed_url.path)
    path_to_files = '{0}/{1}{2}_files'.format(
        output, change_symbols(hostname), path,
    )
    return {
        'original_url': url,
        'scheme': scheme,
        'scheme_with_host': '{0}://{1}'.format(scheme, hostname),
        'host_name': change_symbols(hostname),
        'path_to_html': '{0}/{1}{2}.html'.format(
            output, change_symbols(hostname), path,
        ),
        'path_to_files': path_to_files,
    }


def path_to_file(src, path_builder):
    parsed_src = urlparse(src)
    if parsed_src.scheme:
        parsed_src = (parsed_src._replace(scheme=''))._replace(netloc='')
        src = parsed_src.geturl()
    extension = os.path.splitext(src)[1]
    if not extension:
        src = '{0}.html'.format(src)
    valid_src = change_symbols(src)
    return {
        'absolute': '{0}/{1}{2}'.format(
            path_builder['path_to_files'],
            path_builder['host_name'],
            valid_src,
        ),
        'relative': '{0}/{1}{2}'.format(
            os.path.basename(path_builder['path_to_files']),
            path_builder['host_name'],
            valid_src,
        ),
    }


def change_symbols(part_of_url):
    symbols_to_change = r'[^A-Za-z\d]'
    if part_of_url.startswith('/'):
        root_ext = os.path.splitext(part_of_url)
        path_without_ext = re.sub(symbols_to_change, '-', root_ext[0])
        return '{0}{1}'.format(path_without_ext, root_ext[1])
    return re.sub(symbols_to_change, '-', part_of_url)
