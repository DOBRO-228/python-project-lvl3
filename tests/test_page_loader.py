#!/usr/bin/env python3
"""Tests."""

import os
import tempfile

from page_loader.page_loader import download


def test_download(requests_mock):
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('tests/fixtures/response.html', 'r') as fixture:
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
        requests_mock.get(
            'https://ru.hexlet.io/courses',
            text='<img src="/home/dobro/img.png" alt="И">',
        )
        file_path = download('https://ru.hexlet.io/courses', tmpdir)
        img_path = '{0}_files/ru-hexlet-io-home-dobro-img.png'.format(
            file_path[:-5],
        )
        assert os.path.isfile(img_path)


def test_change_img_url(requests_mock):
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get(
            'https://ru.hexlet.io/courses',
            text='<img src="/home/dobro/img.png" alt="И">',
        )
        file_path = download('https://ru.hexlet.io/courses', tmpdir)
        img_src = 'ru-hexlet-io-courses_files/ru-hexlet-io-home-dobro-img.png'
        with open(file_path, 'r') as html_file:
            assert html_file.read() == '<img src="{0}" alt="И">'.format(img_src)
