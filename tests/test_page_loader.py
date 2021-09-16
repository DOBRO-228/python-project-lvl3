#!/usr/bin/env python3
"""Tests."""

import tempfile
from pathlib import Path

from page_loader.page_loader import download, download_file
from page_loader.path_formatter import path_formatter


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


def test_download_media(requests_mock):
    """Test download image method of page-loader.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        url = 'https://ru.hexlet.io/courses'
        first_image_full_url = '{0}/home/dobro/Pictures/img.png'.format(url)
        second_image_full_url = '{0}/home/dobro/Pictures/img2.jpg'.format(url)
        with open('tests/fixtures/html_with_imgs.html', 'rb') as html_page:
            requests_mock.get('https://ru.hexlet.io/courses', body=html_page)
            file_path = download(url, tmpdir)
            assert file_path == '{0}/ru-hexlet-io-courses.html'.format(tmpdir)

        # url = 'https://cdn2.hexlet.io/derivations/image/original/eyJpZCI6IjMxNzExYTI4ZDZlODlkODMzMThiZWE4MmIxOWViOTM1LnBuZyIsInN0b3JhZ2UiOiJjYWNoZSJ9?signature=83ec1b3027a828ce2e5f6210594bfa33db447da9dc7446b61a6553c8de153572'
        # path_to_img = page_loader.download_img(url, tmpdir)
        # assert imghdr.what(path_to_img) == 'png'


def test_download_img(requests_mock):
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        path_builder = path_formatter('https://ru.hexlet.io/courses', tmpdir)
        image_full_url = '{0}/home/dobro/Pictures/img.png'.format(
            path_builder['original_url'],
        )
        with open('/home/dobro/Pictures/img.png', 'rb') as image:
            requests_mock.get(
                image_full_url, body=image,
            )
            requests_mock.get(
                path_builder['original_url'],
                text='<img src="/home/dobro/Pictures/img.png" alt="И">',
            )
            download('https://ru.hexlet.io/courses', tmpdir)
            path_to_img = '{0}/ru-hexlet-io-home-dobro-Pictures-img.png'.format(
                path_builder['path_to_files'],
            )
            assert Path(path_to_img).exists()


def test_change_img_url(requests_mock):
    """Test download method of page-loader.

    Args:
        requests_mock (package): Package for mocking requests.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        requests_mock.get(
            'https://ru.hexlet.io/courses',
            text='<img src="/home/dobro/Pictures/img.png" alt="И">',
        )
        file_path = download('https://ru.hexlet.io/courses', tmpdir)
        img_src = '{0}/ru-hexlet-io-courses_files/ru-hexlet-io-home-dobro-Pictures-img.png'.format(
            tmpdir,
        )
        with open(file_path, 'r') as html_file:
            assert html_file.read() == '<img src="{0}" alt="И">'.format(img_src)
