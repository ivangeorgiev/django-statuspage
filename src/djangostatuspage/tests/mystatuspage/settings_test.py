import os

os.environ['DJANGO_SECRET_KEY'] = 'secret-key'

from .settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
