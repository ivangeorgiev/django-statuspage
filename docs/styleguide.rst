Styleguide
==========


.. contents:: Table of contents
    :backlinks: top

Practices
---------

Initialize Local Development Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create a directory named ``.dev`` in your local repository copy and use it 
for environment intialization purposes or store some resources that you need during 
development. The ``.dev`` directory is already added to ``.gitignore``.

Inisde the ``.dev`` directory create a ``set_env`` script to initialize environment variables
for the applciation.

Here is an example of Bash ``set_env.sh`` script:

.. code-block:: bash

    #!/bin/sh

    export DJANGO_SECRET_KEY="Very, Very Secret Key. Do not tell anybody!"

And also an example of Windows commdnd file ``set_env.cmd``:

.. code-block:: bat

    @ECHO OFF

    @SET "DJANGO_SECRET_KEY=django-insecure-9312345....9876"


Tokens and Secrets in Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Security tokens and secrets should be stored in environment variables. 
Hardcoded secrets are not allowed.

.. code-block:: python

    import os

    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

Do not use default value when reading the environment variable to enforce target
environment to define the variable and avoid security issues. For local development, 
add the initializaition of the variables to your ``.dev/set_env`` script:

.. code-block:: bash
    
    export DJANGO_SECRET_KEY="Very, Very Secret Key. Do not tell anybody!"


Testing
-------

Group test cases by target
~~~~~~~~~~~~~~~~~~~~~~~~~~

Group related test cases into a test class. For example, to test the ``camel_case_split`` function:

.. code-block:: python

    class TestCamelCaseSplit:
        """Test cases for camel_case_split function"""

        def test_called_with(self):
            result = shortcuts.camel_case_split('PascalCase')
            assert result == ['Pascal', 'Case']

Define test type for each test case
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test cases are grouped by test type (unit, system, etc.). To group tests `pytest marks` are used. 
Each test case can be marked with zero, one or more marks.

Following marks are registered in ``pytest.ini``:

    - ``unit`` - Unit test
    - ``system`` - System test
    - ``integration`` - Integration test
    - ``compat`` - Compatibility test

To mark individual test cases, use the ``@pytest.mark`` decorator:

.. code-block:: python

    import pytest

    @pytest.mark.unit    # Mark following test case as unit test case
    def test_addition():
        assert 2+3 == 5

If ``@pytest.mark`` decorator is applied to a class, all the test cases from the class are marked with the
mark.

To mark all tests in a module define pytestmark module variable and assign to a mark or 
a list of marks:

.. code-block:: python

    pytestmark = pytest.mark.unit    # All test cases in the module 
                                     # are marked as unit test cases

    pytestmark = [pytest.mark.unit, pytest.mark.compat]  # All test cases in the module 
                                                         # are marked as unit and compat test cases


By default ``pytest`` runs only unit tests as specified in ``pytest.ini``.

To execute specific type of tests, e.g. ``system``, pass the type as argument to the ``-m`` option:

.. code-block:: console

    $ pytest -m "system"

To execute all tests pass empty argument to the ``-m`` option:

.. code-block:: console

    $ pytest -m ""

More examples:

.. code-block:: console

    $ # Execute all test cases, but unit tests
    $ pytest -m "not unit"
    $
    $ # Execute only system and integration tests
    $ pytest -m "system or integration"
    $
    $ # Execute only test cases which are system and integration at the same time
    $ pytest -m "system and integration"

To learn more about ``pytest``'s custom marks:

- `Marking test functions with attributes <https://docs.pytest.org/en/6.2.x/mark.html>`_
- `Working with custom markers <https://docs.pytest.org/en/6.2.x/example/markers.html>`_


Test Coverage
~~~~~~~~~~~~~

Measure the test coverage on each test execution. Add corresponding options to ``pytest.ini``:

.. code-block:: ini

    # pytest.ini
    [pytest]
    addopts = 
        -m "unit"
        --cov djangostatuspage
        --cov-report term
        --cov-report html


Git push quality gates
~~~~~~~~~~~~~~~~~~~~~~

Before pushing code to the remote repository make sure that all quality requirements are met:

- All unit tests pass
- Minimal unit test coverage is 80%

To automate these checks, modify the Git pre-push hook in the ``.git/hooks/pre-push`` script:

.. code-block:: bash

    #!/bin/sh

    source .venv310/Scripts/activate
    ./.dev/set_env.sh
    pytest --rootdir=src/djangostatuspage/tests || exit 1
    coverage report --fail-under=80 || exit 1
    exit 0

File layout
~~~~~~~~~~~~

Place tests in ``tests`` module under the application package

1. Create application
2. Create ``tests`` directory
3. Create Django project for tests
4. Configure tests

Test Django Applications with Database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Use in-memory database
2. Use pytest-django
3. Mark test cases or test class which use database with ``@pytest.mark.django_db``



