#!/usr/bin/env python3

"""Logging stuff."""

import logging
import os
import sys
from functools import wraps

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
    log_handler.setFormatter(logging.Formatter(
        '{levelname}: {folder} - {message}', validate=False,
    ))
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
    log_handler.setFormatter(logging.Formatter(
        '{levelname}: {message}', validate=False,
    ))
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
        PermissionError: If we don't have permissions to write into this dir.
    """
    permission_err = "You don't have permissions to write into this directory"
    if not os.path.exists(path):
        raise FileNotFoundError("{0} - Directory doesn't exist".format(path))
    elif not os.path.isdir(path):
        raise NotADirectoryError(
            '{0} - You need to choose a directory, not a file'.format(path),
        )
    elif not os.access(path, os.W_OK):
        raise PermissionError('{0} - {1}'.format(path, permission_err))


def logging_decorator(function):
    """
    Decorate download() function.

    Args:
        function (function): Function to decorate.

    Returns:
        html_path (str): Path to downloaded html

    Raise:
        SystemExit: If any exception will raise.
    """
    @wraps(function)
    def decorator(path, output):
        try:
            html_path = function(path, output)
        except OSError as error:
            os_logger().error(error, extra={'folder': output})
            sys.exit(1)
        except requests.exceptions.RequestException as request_error:
            request_logger().error(request_error)
            sys.exit(1)
        except Exception as error:
            logging.error(error)
            sys.exit(1)
        return html_path
    return decorator


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
