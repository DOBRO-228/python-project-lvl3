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
        'host_name': change_symbols(hostname),
        'path_to_html': '{0}/{1}{2}.html'.format(
            output, change_symbols(hostname), path,
        ),
        'path_to_files': path_to_files,
    }


def path_to_file(src, path_builder):
    return '{0}/{1}{2}'.format(
        path_builder['path_to_files'],
        path_builder['host_name'],
        change_symbols(src),
    )


def change_symbols(part_of_url):
    if part_of_url.startswith('/'):
        root_ext = os.path.splitext(part_of_url)
        path_without_ext = re.sub(r'[^A-Za-z\d]', '-', root_ext[0])
        return '{0}{1}'.format(path_without_ext, root_ext[1])
    return re.sub(r'[^A-Za-z\d]', '-', part_of_url)
