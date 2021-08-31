#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import sys
from urllib.parse import urlparse

import requests

default_path_to_save = os.getcwd()


class PageLoader(object):
    """CLI command which downloads html page from url to path_to_save."""

    def __init__(self):
        self.output = os.getcwd()

    def download(self, url, output=None):
        if output is None:
            output = self.output
        path_to_file = '{0}/{1}'.format(output, format_name_of_file(url))
        with open(path_to_file, 'w') as html_file:
            html_file.write(requests.get(url).text)
            return '{0}\n'.format(path_to_file)


def format_name_of_file(url):
    parsed_url = urlparse(url)
    extracted_path = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
    name_without_extension = ''.join(list(map(
        symbol_changer, list(extracted_path),
    )))
    return '{0}{1}'.format(name_without_extension, '.html')


def symbol_changer(char):
    if char.isalpha() or char.isdigit():
        return char
    return '-'


def download(url_to_download, output=None):
    loader = PageLoader()
    return loader.download(url_to_download, output)


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
        '--output',
        metavar='[dir]',
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
    page_loader = PageLoader()
    sys.stdout.write(page_loader.download(args.url, args.output))


if __name__ == '__main__':
    main()
