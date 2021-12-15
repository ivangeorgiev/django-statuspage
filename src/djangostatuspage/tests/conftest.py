import os
import sys
import django
# sys.path.insert(0, os.path.abspath('..'))
# sys.path.insert(0, os.path.abspath('../src'))

os.environ['DJANGO_SECRET_KEY'] = 'secret-key'
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangostatuspage.tests.mystatuspage.settings'
django.setup()

