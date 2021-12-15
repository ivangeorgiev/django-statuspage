import os
from pathlib import Path
import sys
import django

TESTS_DIR = Path(__file__).resolve().parent
BASE_DIR = TESTS_DIR.parent
sys.path.insert(0, BASE_DIR.absolute())

os.environ['DJANGO_SETTINGS_MODULE'] = 'djangostatuspage.tests.mystatuspage.settings_test'
django.setup()
