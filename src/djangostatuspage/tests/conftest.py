"""Pytest plugin for djangostatuspage testing."""

import os
import sys
from pathlib import Path

import django

TESTS_DIR = Path(__file__).resolve().parent
BASE_DIR = TESTS_DIR.parent
sys.path.insert(0, BASE_DIR.absolute())


def pytest_configure():
    """Configure pytest - pytest hook."""
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangostatuspage.tests.mystatuspage.settings_test'
    django.setup()
