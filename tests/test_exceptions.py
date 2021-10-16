#!/usr/bin/env python3
"""Tests on exceptions."""


import tempfile

import pytest
import requests
from page_loader.page_loader import download


def test_not_found_exception():
    """Test that exception FileNotFoundError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(
            FileNotFoundError, match=".*- Directory doesn't exist$",
        ):
            download(
                'https://ru.hexlet.io/courses',
                '{0}/salam_bratuha'.format(tmpdir),
            )


def test_not_a_dir_exception():
    """Test that exception NotADirectoryError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with open('{0}/file'.format(tmpdir), 'w') as not_a_dir:
            not_a_dir.write('salam, bratva')
        with pytest.raises(
            NotADirectoryError,
            match='.*- You need to choose a directory, not a file$',
        ):
            download('https://ru.hexlet.io/courses', '{0}/file'.format(tmpdir))


def test_permission_exception():
    """Test that exception PermissionError will be raised."""
    with pytest.raises(
        PermissionError,
        match=".*- You don't have permissions to write into this directory$",
    ):
        download('https://ru.hexlet.io/courses', '/')


def test_http_exception():
    """Test that exception requests.exceptions.HTTPError will be raised."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(
            requests.exceptions.HTTPError,
            match='404 Client Error: Not Found for url: .*$',
        ):
            download('https://ru.hexlet.io/courses1488228', tmpdir)
