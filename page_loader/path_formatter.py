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
        'full_url': '{0}{1}'.format(hostname, path),
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
    only_with_dashes = ''.join(
        [symbol_changer(char) for char in list(path)],
    )
    return re.sub('-(?=jpg|png)', '.', only_with_dashes)


def symbol_changer(char):
    if char.isalpha() or char.isdigit():
        return char
    return '-'
