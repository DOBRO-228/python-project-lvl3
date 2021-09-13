#!/usr/bin/env python3

"""Path formatter."""

from urllib.parse import urlparse


class PathFormatter(object):

    def __init__(self, url, output):
        self.url = url
        self.output = output

    @property
    def path_to_html(self):
        parsed_url = urlparse(self.url)
        path = '{0}{1}'.format(parsed_url.netloc, parsed_url.path)
        self.change_symbols(path)
        return '{0}/{1}.html'.format(self.output, path)

    def change_symbols(self, path):
        path = ''.join(list(map(self.symbol_changer, list(path))))

    def symbol_changer(self, char):
        if char.isalpha() or char.isdigit():
            return char
        return '-'