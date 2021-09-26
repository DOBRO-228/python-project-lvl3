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
    if output == os.getcwd():
        path_to_files = '{0}{1}_files'.format(
            change_symbols(hostname), path,
        )
    else:
        path_to_files = '{0}/{1}{2}_files'.format(
            output, change_symbols(hostname), path,
        )
    return {
        'original_url': url,
        'scheme': scheme,
        'scheme_with_host': '{0}://{1}'.format(scheme, hostname),
        'host_name': change_symbols(parsed_url.netloc),
        'path_to_html': '{0}/{1}{2}.html'.format(
            output, change_symbols(hostname), path,
        ),
        'path_to_files': path_to_files,
    }


def path_to_file(src, path_builder):
    if path_builder['scheme'] in src:
        src = src.replace(path_builder['scheme_with_host'], '')
    last_paths_node = re.sub(r'.*\/(?=.+$)', '', src)
    if '.' not in last_paths_node:
        src = '{0}.html'.format(src)
    return '{0}/{1}{2}'.format(
        path_builder['path_to_files'],
        path_builder['host_name'],
        change_symbols(src),
    )


def change_symbols(path):
    if path.startswith('/') and '.' in path:
        path_with_dashes = re.sub(r'[^A-Za-z\d](?=.*\.)', '-', path)
    else:
        path_with_dashes = re.sub(r'[^A-Za-z\d]', '-', path)
    return re.sub('-(?=jpg|png)', '.', path_with_dashes)
