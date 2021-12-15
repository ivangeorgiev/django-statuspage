How-To
======


Django
-------

Document Django project using Sphinx
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add at the beginning of the ``docs/conf.py`` following:

.. code-block:: python

    import os
    import sys
    import django
    sys.path.insert(0, os.path.abspath('..'))
    sys.path.insert(0, os.path.abspath('../src'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'djangostatuspage.tests.mystatuspage.settings'
    django.setup()

Further reading:

- `How to document your Django project using the Sphinx tool <https://www.freecodecamp.org/news/sphinx-for-django-documentation-2454e924b3bc/>`_

Create Django project
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ django-admin startproject mystatuspage

For further reference see also:

- `Django tutorial <https://docs.djangoproject.com/en/4.0/intro/tutorial01/>`_
- `How to Create a Basic Project using MVT in Django ? <https://www.geeksforgeeks.org/how-to-create-a-basic-project-using-mvt-in-django>`_

Create basic Django App:
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    $ django-admin startapp djangostatuspage

or in the context of Django project:

.. code-block:: console

    $ python manage.py startapp djangostatuspage

Continuous Integration (CI)
---------------------------

Codecov
~~~~~~~~

For `codecov <https://app.codecov.io/gh>` integration, CI tool needs to provide XML report from unit test execution.

No token is required for public repositories.

For example you need to use following in your ``.travis.yml``:

.. code-block:: yml

    language: python
    python:
      - "3.8"
      - "3.9"
      # - "3.10" # Travis fails to install Python 3.10
      - "nightly"  # nightly build

    before_install:
      - pip install codecov

    after_success:
      - codecov

    install:
      - pip install -r requirements.txt

    script:
      - pytest src/djangostatuspage/tests --cov-report xml


