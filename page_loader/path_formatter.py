#!/usr/bin/env python3

"""Path formatter."""

import os
import re
from urllib.parse import urlparse


def path_formatter(url, output):
    """
    Build(format) path.

    Args:
        url (str): URL to download.
        output (str): Where to download.

    Returns:
        (dict): Dictionary with paths.
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    hostname = parsed_url.netloc
    path = parsed_url.path
    path = '' if path == '/' else path
    path_to_files = '{0}/{1}{2}_files'.format(
        output, change_symbols(hostname), change_symbols(path),
    )
    return {
        'original_url': url,
        'scheme_with_host': '{0}://{1}'.format(scheme, hostname),
        'host_name': change_symbols(hostname),
        'path_to_html': '{0}/{1}{2}.html'.format(
            output, change_symbols(hostname), change_symbols(path),
        ),
        'path_to_files': path_to_files,
    }


def path_to_file(src, path_builder):
    """
    Build path to downloaded file.

    Args:
        src (str): URL to download.
        path_builder (dict): Paths.

    Returns:
        (dict): Dictionary with absolute and relative path to file.
    """
    parsed_src = urlparse(src)
    if parsed_src.netloc and parsed_src.path == '/':
        parsed_src = ((  # noqa: WPS437
            parsed_src._replace(scheme='')  # noqa: WPS437
        )._replace(path='')
        )._replace(netloc='')
    elif parsed_src.scheme:
        parsed_src = ((  # noqa: WPS437
            parsed_src._replace(scheme='')  # noqa: WPS437
        )._replace(netloc='')
        )._replace(query='')
    src = parsed_src.geturl()
    src_without_ext, extension = os.path.splitext(src)
    valid_src = change_symbols(src_without_ext)
    if extension:
        valid_src = '{0}{1}'.format(valid_src, extension)
    else:
        valid_src = '{0}.html'.format(valid_src)
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
    """
    Change symbols.

    Args:
        part_of_url (str): Part of URL.

    Returns:
        (str): Part of URL with changed symbols.
    """
    return re.sub(r'[^A-Za-z\d]', '-', part_of_url)
