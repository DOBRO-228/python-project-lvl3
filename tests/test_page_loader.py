#!/usr/bin/env python3
"""Tests."""

import os
import re
import tempfile
from typing import Union
from urllib.parse import urljoin

from page_loader.page_loader import download
from page_loader.path_formatter import path_formatter


def read(path: str, mode: str = 'r') -> Union[str, bytes]:
    """
    Read file.

    Args:
        path (str): Path to file.
        mode (str): Reading mode.

    Returns:
        Union[str, bytes]: Insides.
    """
    with open(path, mode) as opened_file:
        return opened_file.read()


def test_download(requests_mock):
    """
    Test that download function will download html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get('https://ru.hexlet.io/courses', text='html_page')
        file_path = download('https://ru.hexlet.io/courses', tmpdir)
        assert file_path == '{0}/ru-hexlet-io-courses.html'.format(tmpdir)
        with open(file_path, 'r') as html_file:
            assert html_file.read() == read(
                'tests/fixtures/expected_htmls/response.html', 'r',
            )


def test_download_img(requests_mock):
    """
    Test that download function will download image from html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        image_full_url = urljoin(
            path_builder['original_url'], '/tests/fixtures/files/img.png',
        )
        requests_mock.get(
            image_full_url, content=read('tests/fixtures/files/img.png', 'rb'),
        )
        requests_mock.get(
            path_builder['original_url'],
            text='<img src="/tests/fixtures/files/img.png" alt="И">',
        )
        download('https://ru.hexlet.io/courses', tmpdir)
        path_to_img = '{0}/ru-hexlet-io-tests-fixtures-files-img.png'.format(
            path_builder['path_to_files'],
        )
        assert read(path_to_img, 'rb') == read(
            'tests/fixtures/files/img.png', 'rb',
        )


def test_download_all_media(requests_mock):
    """
    Test that download function will download all media from html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        requests_mock.get(
            'https://ru.hexlet.io/courses',
            text=read('tests/fixtures/html_with_imgs.html', 'r'),
        )
        requests_mock.get(
            'https://ru.hexlet.io/tests/fixtures/files/img.png',
            content=read('tests/fixtures/files/img.png', 'rb'),
        )
        requests_mock.get(
            'https://ru.hexlet.io/tests/fixtures/files/img2.jpg',
            content=read('tests/fixtures/files/img2.jpg', 'rb'),
        )
        requests_mock.get(
            'https://ru.hexlet.io/tests/fixtures/files/application.css',
            text=read('tests/fixtures/files/application.css', 'r'),
        )
        requests_mock.get(
            'https://ru.hexlet.io/packs/js/script.js',
            text=read('tests/fixtures/files/script.js', 'r'),
        )
        download('https://ru.hexlet.io/courses', tmpdir)
        path_to_files = path_builder['path_to_files']
        assert read(
            '{0}/ru-hexlet-io-packs-js-script.js'.format(
                path_to_files,
            ),
            'r',
        ) == read('tests/fixtures/files/script.js', 'r')
        downloaded_files = os.listdir(path_to_files)
        assert len(downloaded_files) == 5
        assert read(
            '{0}/ru-hexlet-io-tests-fixtures-files-application.css'.format(
                path_to_files,
            ), 'r',
        ) == read('tests/fixtures/files/application.css', 'r')
        dwnld_jpg = '{0}/ru-hexlet-io-tests-fixtures-files-img2.jpg'.format(
            path_to_files,
        )
        assert read(dwnld_jpg, 'rb') == read(
            'tests/fixtures/files/img2.jpg', 'rb',
        )
        assert read(
            '{0}/ru-hexlet-io-tests-fixtures-files-img.png'.format(
                path_to_files,
            ), 'rb',
        ) == read(
            'tests/fixtures/files/img.png', 'rb',
        )


def test_change_files_src(requests_mock):
    """
    Test that sources of files will be replaced on local sources in html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter(
            'https://ru.hexlet.io/courses', tmpdir,
        )
        requests_mock.get(
            re.compile(r'.*hexlet\.io.*'),
            text=read('tests/fixtures/html_with_files.html', 'r'),
        )
        html_file = download(path_builder['original_url'], tmpdir)
        exp_html_file = 'tests/fixtures/expected_htmls/exp_html_sources.html'
        assert read(html_file, 'r') == read(exp_html_file, 'r')
