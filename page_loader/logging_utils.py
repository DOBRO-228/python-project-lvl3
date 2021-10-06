#!/usr/bin/env python3

"""Loggers and checks."""

import logging
import os

import requests


def os_logger():
    logger = logging.getLogger('os')
    logger.setLevel(logging.ERROR)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter('{levelname}: {folder} - {message}', validate=False))
    logger.addHandler(log_handler)
    return logger


def request_logger():
    logger = logging.getLogger('request')
    logger.setLevel(logging.ERROR)
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(logging.Formatter('{levelname}: {message}', validate=False))
    logger.addHandler(log_handler)
    return logger


def check_folder(path):
    if not os.path.exists(path):
        raise FileNotFoundError("{0} - Folder doesn't exist".format(path))
    elif not os.path.isdir(path):
        raise NotADirectoryError('{0} - You need to choose a folder, not a file'.format(path))
    elif not os.access(path, os.W_OK):
        raise PermissionError("{0} - You don't have permissions to write into this folder".format(path))


def request_wrapper(url):
    res = requests.get(url)
    not_expected_status = 399
    if res.status_code > not_expected_status:
        res.raise_for_status()
    return res
