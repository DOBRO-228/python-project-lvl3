#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import pathlib
import types
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from page_loader.logging_utils import check_folder, info_logger
from page_loader.logging_utils import logging_decorator as logging
from page_loader.logging_utils import request_wrapper
from page_loader.path_formatter import path_formatter, path_to_file
from progress.bar import FillingSquaresBar


def download(url, output=None):
    """
    Download html and local resources.

    Args:
        url (str): URL to download.
        output (str): Where to download.

    Returns:
        (str): Path to html file.
    """
    if output is None and output != '':
        output = os.getcwd()
    check_folder(output)
    path_builder = path_formatter(url, output)
    html = request_wrapper(url).text
    soup = BeautifulSoup(html, 'html.parser')
    download_files(path_builder, soup)
    with open(path_builder['path_to_html'], 'w') as html_file:
        html_file.write(soup.prettify())
    return path_builder['path_to_html']


SOURCES = types.MappingProxyType({
    'img': 'src',
    'script': 'src',
    'link': 'href',
})


def download_files(path_builder, soup):
    """
    Download local resources.

    Args:
        path_builder (dict): URL to download.
        soup (bs4.BeautifulSoup): Soup.
    """
    pathlib.Path(path_builder['path_to_files']).mkdir(
        parents=False, exist_ok=True,
    )
    elements_to_download = []
    for html_elem in soup.find_all(SOURCES.keys()):
        file_src = html_elem.get(SOURCES[html_elem.name])
        if file_src is not None:
            file_src = urljoin(
                path_builder['original_url'],
                file_src,
            )
            if file_src.startswith(path_builder['scheme_with_host']):
                html_elem[SOURCES[html_elem.name]] = file_src
                elements_to_download.append(html_elem)
    with FillingSquaresBar(
        'Downloading files',
        max=len(elements_to_download),
    ) as progress_bar:
        for element in elements_to_download:
            element[SOURCES[element.name]] = download_file(
                element[SOURCES[element.name]], path_builder,
            )
            progress_bar.next()


def download_file(src, path_builder):
    """
    Download one resource.

    Args:
        src (str): URL to download.
        path_builder (dict): Absolute and relative paths to file.

    Returns:
        (str): Path to downloaded file.
    """
    with open(path_to_file(src, path_builder)['absolute'], 'wb') as inner_file:
        inner_file.write(request_wrapper(src).content)
    return path_to_file(src, path_builder)['relative']


def main():
    """CLI command."""
    parser = argparse.ArgumentParser(
        usage='page-loader [options] <url>',
        description='Download html page',
        argument_default=argparse.SUPPRESS,
        add_help=False,
    )
    group = parser.add_argument_group('Options')
    group.add_argument(
        '-o',
        '--output',
        help='output dir (default: cwd)',
        default=os.getcwd(),
    )
    group.add_argument(
        '-h',
        '--help',
        action='help',
        help='display help for command',
    )
    parser.add_argument(
        'url',
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()
    file_path = logging(download)(args.url, args.output)
    msg_about_success = 'Page was successfully downloaded into'
    info_logger().info("{0} '{1}'".format(msg_about_success, file_path))


if __name__ == '__main__':
    main()
