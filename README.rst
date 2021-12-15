Django Status Page Plugin
=========================

.. image:: https://app.travis-ci.com/ivangeorgiev/django-statuspage.svg?branch=main
    :target: https://app.travis-ci.com/ivangeorgiev/django-statuspage

.. image:: https://readthedocs.org/projects/django-statuspage/badge/?version=latest
    :target: https://django-statuspage.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

System Status Page in Django

Django Status Page documentation is available on `Github pages <https://ivangeorgiev.github.io/django-statuspage/>`_ as well as on `Read the docs <https://django-statuspage.readthedocs.io/en/latest/>`_. 

Installation - Development Environment
--------------------------------------

To install the package, you need to checkout the source repository and use ``pip`` to install 
dependencies:

.. code-block:: console

    $ git clone https://github.com/ivangeorgiev/django-statuspage
    $ cd django-statuspage
    $ pip install -U -r requirements.txt


Build and Test
--------------

Test
~~~~

Django Status Page uses `pytest <https://docs.pytest.org/>`_ as test framework. To execute the tests run the ``pytest`` command:

.. code-block:: console

    $ pytest src/djangostatuspage/tests


Build Documentation
~~~~~~~~~~~~~~~~~~~

Documentation sources are stored in the ``docs`` directory. It is written using 
`reStructuredText <https://docutils.sourceforge.io/rst.html>`_ and uses `Sphinx <https://www.sphinx-doc.org/en/master/>`_ to build user documentation.

To build documentation use the ``make`` script from the ``docs`` directory:

.. code-block:: console

    cd docs
    make html

The output will be stored in the ``docs/_build/html`` directory.

You can also build and publish the Github pages using the ``.publish.sh`` script:

.. code-block:: console

    cd docs
    . .publish.sh

The script will build the HTML documentation, checkout the Github pages branch into the ``docs/_build/.build``
directory, stage and push the changes to Github.




