#!/usr/bin/env python3
"""Tests."""

import tempfile

from page_loader.page_loader import download


def test_download_path():
    """Tests generated files path of download function.

    Returns answer of assert.
    """
    with tempfile.TemporaryDirectory() as tmpdirname:
        file_path = download('https://ru.hexlet.io/courses', tmpdirname)
        expected_path = '{0}/ru-hexlet-io-courses.html'.format(tmpdirname)
        assert file_path == expected_path
