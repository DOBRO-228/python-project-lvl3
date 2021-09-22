#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import pathlib
import sys

import requests
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
from page_loader.path_formatter import path_formatter, path_to_file


class UnsortedAttrsHtml5(HTMLFormatter):
    def attributes(self, tag):
        self.void_element_close_prefix = None
        for k, v in tag.attrs.items():
            yield k, v


def download(url, output=None):
    if output is None:
        output = os.getcwd()
    path_builder = path_formatter(url, output)
    download_html(path_builder)
    download_files(path_builder)
    return path_builder['path_to_html']


def download_html(path_builder):
    with open(path_builder['path_to_html'], 'w') as html_file:
        html_file.write(requests.get(path_builder['original_url']).text)


def download_files(path_builder):
    pathlib.Path(path_builder['path_to_files']).mkdir(
        parents=True, exist_ok=True,
    )
    with open(path_builder['path_to_html'], 'r') as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')
        for html_elem in soup.find_all('img'):
            file_src = html_elem.get('src')
            if file_src.startswith('/'):
                html_elem['src'] = download_file(
                    file_src,
                    path_builder,
                )
        rewrite_html_file(path_builder['path_to_html'], soup)


def rewrite_html_file(html_file, soup):
    with open(html_file, 'w') as new_html_file:
        new_html_file.write(soup.encode(
            formatter=UnsortedAttrsHtml5(),
        ).decode('utf-8'),
        )


def download_file(src, path_builder):
    url_to_download = '{0}{1}'.format(path_builder['original_url'], src)
    response = requests.get(url_to_download)
    with open(path_to_file(src, path_builder), 'wb') as inner_file:
        inner_file.write(response.content)
    return path_to_file(src, path_builder)


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
        metavar='--output',
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
    file_path = '{0}\n'.format(download(args.url, args.o))
    sys.stdout.write(file_path)


if __name__ == '__main__':
    main()
