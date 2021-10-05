#!/usr/bin/env python3
"""Tests."""

import os
import re
import shutil
import tempfile

import pytest
import requests
from page_loader.page_loader import download
from page_loader.path_formatter import path_formatter


def test_download(requests_mock):
    """Test download method of page-loader.

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
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        image_full_url = '{0}/tests/fixtures/files/img.png'.format(
            path_builder['original_url'],
        )
        with open('tests/fixtures/files/img.png', 'rb') as image:
            requests_mock.get(
                image_full_url, body=image,
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
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        with open('tests/fixtures/html_with_imgs.html', 'rb') as html_page:
            matcher = re.compile(r'.*hexlet\.io.*')
            requests_mock.get(matcher, body=html_page)
            download('https://ru.hexlet.io/courses', tmpdir)
            files = os.listdir(path_builder['path_to_files'])
            assert len(files) == 2


def test_change_files_src(requests_mock):
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree(os.getcwd(), tmpdir, dirs_exist_ok=True)
        os.chdir(tmpdir)
        path_builder = path_formatter(
            'https://ru.hexlet.io/courses', os.getcwd(),
        )
        path_to_fixture = '{0}/tests/fixtures/html_with_files.html'.format(tmpdir)
        with open(path_to_fixture, 'rb') as html_page:
            requests_mock.get(
                re.compile(r'.*hexlet\.io.*'),
                body=html_page,
            )
            file_path = download(path_builder['original_url'])
            with open(file_path, 'r') as html_file:
                path_to_expctd_fixture = '{0}/tests/fixtures/expected_htmls/expected_html_sources.html'.format(tmpdir)
                with open(path_to_expctd_fixture, 'r') as expected_html_file:
                    assert html_file.read() == expected_html_file.read()


def test_not_found_exception():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(FileNotFoundError, match=".*- Folder doesn't exist$"):
            download('https://ru.hexlet.io/courses', '{0}/salam_bratuha'.format(tmpdir))


def test_not_a_dir_exception():
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('{0}/file'.format(tmpdir), 'w') as file:
            file.write('salam, bratva')
        with pytest.raises(NotADirectoryError, match='.*- You need to choose a folder, not a file$'):
            download('https://ru.hexlet.io/courses', '{0}/file'.format(tmpdir))


def test_permission_exception():
    with pytest.raises(PermissionError, match=".*- You don't have permissions to write into this folder$"):
        download('https://ru.hexlet.io/courses', '/')


def test_http_exception():
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with pytest.raises(requests.exceptions.HTTPError, match='404 Client Error: Not Found for url: .*$'):
            download('https://ru.hexlet.io/courses1488228', tmpdir)
