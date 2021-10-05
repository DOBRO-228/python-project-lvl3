#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import logging
import os
import pathlib
import sys
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
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
    parsed_src = urlparse(src)
    if parsed_src.scheme:
        url_to_download = src
        parsed_src = (parsed_src._replace(scheme=''))._replace(netloc='')
        src = parsed_src.geturl()
    else:
        url_to_download = '{0}{1}'.format(path_builder['original_url'], src)
    extension = os.path.splitext(src)[1]
    if not extension:
        src = '{0}.html'.format(src)
    with open(path_to_file(src, path_builder), 'wb') as inner_file:
        inner_file.write(request_wrapper(url_to_download).content)
    return path_to_file(src, path_builder)


def check_folder(path):
    if not os.path.exists(path):
        raise FileNotFoundError("{0} - Folder doesn't exist".format(path))
    elif not os.path.isdir(path):
        raise NotADirectoryError('{0} - You need to choose a folder, not a file'.format(path))
    elif not os.access(path, os.W_OK):
        raise PermissionError("{0} - You don't have permissions to write into this folder".format(path))


def request_wrapper(url):
    res = requests.get(url)
    not_expected_status = 399
    if res.status_code > not_expected_status:
        res.raise_for_status()
    return res


def main():
    parser = argparse.ArgumentParser(
        usage='page-loader [options] <url>',
        description='Download html page',
        argument_default=argparse.SUPPRESS,
        add_help=False,
    )
    parser.add_argument(
        'url',
        help=argparse.SUPPRESS,
    )
    group = parser.add_argument_group('Options')
    group.add_argument(
        '-o',
        metavar=('--output', '[dir]'),
        nargs=2,
        help='output dir (default: "/app")',
        default=os.getcwd(),
    )
    group.add_argument(
        '-h',
        '--help',
        action='help',
        help='display help for command',
    )
    args = parser.parse_args()
    logging.basicConfig(
        format='%(levelname)s: %(folder)s - %(message)s',
        level=logging.ERROR,
        stream=sys.stderr,
    )
    try:
        check_folder(args.o)
    except OSError as error:
        logging.error(error, extra={'folder': args.o})
        sys.exit(1)
    try:
        file_path = '{0}\n'.format(download(args.url, args.o))
    except requests.exceptions.RequestException as request_error:
        logging.error(request_error, extra={'folder': ''})
        sys.exit(1)
    sys.stdout.write(file_path)


if __name__ == '__main__':
    main()
