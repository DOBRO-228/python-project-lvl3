#!/usr/bin/env python3
"""Tests."""

import os
import re
import tempfile
from urllib.parse import urljoin

import pytest
import requests
from page_loader.page_loader import download
from page_loader.path_formatter import path_formatter


def test_download(requests_mock):
    """
    Test that download function will download html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('tests/fixtures/expected_htmls/response.html', 'r') as fixture:
            requests_mock.get('https://ru.hexlet.io/courses', text='html_page')
            file_path = download('https://ru.hexlet.io/courses', tmpdir)
            assert file_path == '{0}/ru-hexlet-io-courses.html'.format(tmpdir)
            with open(file_path, 'r') as html_file:
                assert html_file.read() == fixture.read()


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
        with open('tests/fixtures/files/img.png', 'rb') as image:
            requests_mock.get(
                image_full_url, content=image.read(),
            )
            requests_mock.get(
                path_builder['original_url'],
                text='<img src="/tests/fixtures/files/img.png" alt="И">',
            )
            download('https://ru.hexlet.io/courses', tmpdir)
            path_to_img = '{0}/ru-hexlet-io-tests-fixtures-files-img.png'.format(
                path_builder['path_to_files'],
            )
            with open(path_to_img, 'rb') as downloaded_image:
                with open('tests/fixtures/files/img.png', 'rb') as original_image:
                    assert downloaded_image.read() == original_image.read()


def test_download_all_media(requests_mock):
    """
    Test that download function will download all media from html page.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        with open('tests/fixtures/html_with_imgs.html', 'r') as html_page:
            requests_mock.get('https://ru.hexlet.io/courses', text=html_page.read())
        with open('tests/fixtures/files/img.png', 'rb') as original_png:
            requests_mock.get('https://ru.hexlet.io/tests/fixtures/files/img.png', content=original_png.read())
        with open('tests/fixtures/files/img2.jpg', 'rb') as original_jpg:
            requests_mock.get('https://ru.hexlet.io/tests/fixtures/files/img2.jpg', content=original_jpg.read())
        with open('tests/fixtures/files/application.css', 'r') as original_css:
            requests_mock.get('https://ru.hexlet.io/tests/fixtures/files/application.css', text=original_css.read())
        with open('tests/fixtures/files/script.js', 'r') as original_js:
            requests_mock.get('https://ru.hexlet.io/packs/js/script.js', text=original_js.read())
        download('https://ru.hexlet.io/courses', tmpdir)
        with open('{0}/ru-hexlet-io-packs-js-script.js'.format(path_builder['path_to_files']), 'r') as downloaded_js:
            with open('tests/fixtures/files/script.js', 'r') as expected_js:
                assert downloaded_js.read() == expected_js.read()
                files = os.listdir(path_builder['path_to_files'])
                assert len(files) == 5
        with open(
            '{0}/ru-hexlet-io-tests-fixtures-files-application.css'.format(path_builder['path_to_files']),
            'r',
        ) as downloaded_css:
            with open('tests/fixtures/files/application.css', 'r') as expected_css:
                assert downloaded_css.read() == expected_css.read()
        with open(
            '{0}/ru-hexlet-io-tests-fixtures-files-img2.jpg'.format(path_builder['path_to_files']),
            'rb',
        ) as downloaded_jpg:
            with open('tests/fixtures/files/img2.jpg', 'rb') as expected_jpg:
                assert downloaded_jpg.read() == expected_jpg.read()
        with open(
            '{0}/ru-hexlet-io-tests-fixtures-files-img.png'.format(path_builder['path_to_files']),
            'rb',
        ) as downloaded_png:
            with open('tests/fixtures/files/img.png', 'rb') as expected_png:
                assert downloaded_png.read() == expected_png.read()


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
        with open('tests/fixtures/html_with_files.html', 'r') as html_page:
            requests_mock.get(
                re.compile(r'.*hexlet\.io.*'),
                text=html_page.read(),
            )
            with open(download(path_builder['original_url'], tmpdir), 'r') as html_file:
                with open('tests/fixtures/expected_htmls/expected_html_sources.html', 'r') as expected_html_file:
                    assert html_file.read() == expected_html_file.read()


def test_not_found_exception():
    """Test that exception FileNotFoundError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError, match=".*- Folder doesn't exist$"):
            download('https://ru.hexlet.io/courses', '{0}/salam_bratuha'.format(tmpdir))


def test_not_a_dir_exception():
    """Test that exception NotADirectoryError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('{0}/file'.format(tmpdir), 'w') as file:
            file.write('salam, bratva')
        with pytest.raises(NotADirectoryError, match='.*- You need to choose a folder, not a file$'):
            download('https://ru.hexlet.io/courses', '{0}/file'.format(tmpdir))


def test_permission_exception():
    """Test that exception PermissionError will be raised."""
    with pytest.raises(PermissionError, match=".*- You don't have permissions to write into this folder$"):
        download('https://ru.hexlet.io/courses', '/')


def test_http_exception():
    """Test that exception requests.exceptions.HTTPError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(requests.exceptions.HTTPError, match='404 Client Error: Not Found for url: .*$'):
            download('https://ru.hexlet.io/courses1488228', tmpdir)
