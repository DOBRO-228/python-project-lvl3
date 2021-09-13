#!/usr/bin/env python3

"""Page loader cli."""

import argparse
import os
import sys
from shutil import copy2

import requests
from bs4 import BeautifulSoup
from page_loader.path_formatter import PathFormatter


class PageLoader(object):
    """CLI command which downloads html page from url to path_to_save."""

    def __init__(self, url):
        self.path_formatter = PathFormatter(url)

    def download(self, output=None):
        if output is None:
            output = os.getcwd()
        path_to_html = self.download_html(
            self.path_formatter.path_to_html, output,
        )
        self.download_media(self.path_formatter.path_to_media, output)
        return path_to_html

    def download_html(self, url, output):
        where_to_save = '{0}/{1}'.format(output, self.format_path(url, 'html'))
        with open(where_to_save, 'w') as html_file:
            html_file.write(requests.get(url).text)
        return where_to_save

    def download_media(self, path_to_html, output):
        path_to_dir = path_to_html.replace('.html', '_files')
        with open(path_to_html) as html_file:
            soup = BeautifulSoup(html_file, 'html.parser')
            print(soup.prettify())
            print(soup.find_all('img'))
            for image in soup.find_all('img'):
                self.download_img(image.get('src'), path_to_dir)

    def download_img(self, url, directory):
        path_to_file = '{0}/img.png'.format(directory)
        if url.startswith('/'):
            copy2(url, path_to_file)
        else:
            response = requests.get(url)
            with open(path_to_file, 'wb') as img:
                img.write(response.content)
        return path_to_file


def download(url, output=None):
    downloader = PageLoader(url, output)
    return downloader.download(output)


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
    file_path = '{0}\n'.format(page_loader.download(args.url, args.output))
    sys.stdout.write(file_path)


if __name__ == '__main__':
    main()
