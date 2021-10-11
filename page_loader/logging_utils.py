#!/usr/bin/env python3

"""Logging stuff."""

import logging
import os

import requests


def os_logger():
    """
    Logger for OS exceptions.

    Level - ERROR

    Returns:
        logger
    """
    logger = logging.getLogger('os')
    logger.setLevel(logging.ERROR)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter('{levelname}: {folder} - {message}', validate=False))
    logger.addHandler(log_handler)
    return logger


def request_logger():
    """
    Logger for requests exceptions.

    Level - ERROR

    Returns:
        logger
    """
    logger = logging.getLogger('request')
    logger.setLevel(logging.ERROR)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter('{levelname}: {message}', validate=False))
    logger.addHandler(log_handler)
    return logger


def info_logger():
    """
    Logger for informing user.

    Level - INFO

    Returns:
        logger
    """
    logger = logging.getLogger('info')
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    return logger


def check_folder(path):
    """
    Raise OS exception if we can't write into directory.

    Args:
        path (str): Path to directory.

    Raises:
        FileNotFoundError: If directory doesn't exist.
        NotADirectoryError: If it isn't a directory.
        PermissionError: If we don't have permissions to write into this directory.
    """
    if not os.path.exists(path):
        raise FileNotFoundError("{0} - Directory doesn't exist".format(path))
    elif not os.path.isdir(path):
        raise NotADirectoryError('{0} - You need to choose a directory, not a file'.format(path))
    elif not os.access(path, os.W_OK):
        raise PermissionError("{0} - You don't have permissions to write into this directory".format(path))


def request_wrapper(url):
    """
    Raise exception if status code > 399.

    Args:
        url (str): URL to download.

    Returns:
        res (object): Request's response.
    """
    res = requests.get(url)
    not_expected_status = 399
    if res.status_code > not_expected_status:
        res.raise_for_status()
    return res
