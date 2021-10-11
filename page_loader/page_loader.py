#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import pathlib
import sys
import types
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from page_loader.logging_utils import (
    check_folder,
    info_logger,
    os_logger,
    request_logger,
    request_wrapper,
)
from page_loader.path_formatter import path_formatter, path_to_file
from progress.bar import FillingSquaresBar


def download(url, output=None):
    if output is None:
        output = os.getcwd()
    check_folder(output)
    path_builder = path_formatter(url, output)
    html = request_wrapper(url).text
    soup = BeautifulSoup(html, 'html.parser')
    download_files(path_builder, soup)
    with open(path_builder['path_to_html'], 'w') as html_file:
        html_file.write(soup.prettify(formatter='html5'))
    return path_builder['path_to_html']


SOURCES = types.MappingProxyType({
    'img': 'src',
    'script': 'src',
    'link': 'href',
})


def download_files(path_builder, soup):
    pathlib.Path(path_builder['path_to_files']).mkdir(
        parents=False, exist_ok=True,
    )
    elements_to_download = []
    for html_elem in soup.find_all(['img', 'script', 'link']):
        file_src = html_elem.get(SOURCES[html_elem.name])
        if file_src is not None:
            if file_src.startswith('/'):
                html_elem[SOURCES[html_elem.name]] = urljoin(path_builder['original_url'], file_src)
                elements_to_download.append(html_elem)
            if file_src.startswith(path_builder['scheme_with_host']):
                elements_to_download.append(html_elem)
    progress_bar = FillingSquaresBar('Downloading files', max=len(elements_to_download))
    for element in elements_to_download:
        element[SOURCES[element.name]] = download_file(
            element[SOURCES[element.name]], path_builder,
        )
        progress_bar.next()
    progress_bar.finish()


def download_file(src, path_builder):
    with open(path_to_file(src, path_builder)['absolute'], 'wb') as inner_file:
        inner_file.write(request_wrapper(src).content)
    return path_to_file(src, path_builder)['relative']


def main():
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
        help='output dir (default: "/app")',
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
    try:
        check_folder(args.output)
    except OSError as error:
        os_logger().error(error, extra={'folder': args.output})
        sys.exit(1)
    try:
        file_path = download(args.url, args.output)
    except requests.exceptions.RequestException as request_error:
        request_logger().error(request_error)
        sys.exit(1)
    info_logger().info("Page was successfully downloaded into '{0}'".format(file_path))


if __name__ == '__main__':
    main()
