#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import pathlib
import sys
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from page_loader.logging_utils import (
    check_folder,
    os_logger,
    request_logger,
    request_wrapper,
)
from page_loader.path_formatter import path_formatter, path_to_file


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


def download_files(path_builder, soup):
    pathlib.Path(path_builder['path_to_files']).mkdir(
        parents=False, exist_ok=True,
    )
    sources = {
        'img': 'src',
        'script': 'src',
        'link': 'href',
    }
    for html_elem in soup.find_all(['img', 'script', 'link']):
        file_src = html_elem.get(sources[html_elem.name])
        if file_src is not None and file_src.startswith(('/', path_builder['scheme_with_host'])):
            html_elem[sources[html_elem.name]] = download_file(
                file_src, path_builder,
            )


def download_file(src, path_builder):
    if urlparse(src).scheme:
        url_to_download = src
    else:
        url_to_download = urljoin(path_builder['original_url'], src)
    with open(path_to_file(src, path_builder)['absolute'], 'wb') as inner_file:
        inner_file.write(request_wrapper(url_to_download).content)
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
        file_path = '{0}\n'.format(download(args.url, args.output))
    except requests.exceptions.RequestException as request_error:
        request_logger().error(request_error)
        sys.exit(1)
    sys.stdout.write(file_path)


if __name__ == '__main__':
    main()
