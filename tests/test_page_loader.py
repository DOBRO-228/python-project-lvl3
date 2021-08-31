#!/usr/bin/env python3
"""Tests."""

import tempfile

from page_loader.page_loader import download


def test_download(requests_mock):
    """Test download method of page-loader .

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
