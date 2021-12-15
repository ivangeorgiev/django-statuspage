Django Status Page Plugin
=========================

System Status Page in Django

Build
-----

Build Documentation
~~~~~~~~~~~~~~~~~~~

Documentation is stored in the ``docs`` directory. It is written using 
`reStructuredText <https://docutils.sourceforge.io/rst.html>`_ and uses `Sphinx <https://www.sphinx-doc.org/en/master/>`_ to build user documentation.

To build documentation use the ``make`` script from the ``docs`` directory:

.. code-block:: console

    cd docs
    make html

The output will be stored in the ``docs/_build/html`` directory.

You can also build and publish the Github pages:

.. code-block:: console

    cd docs
    . .publish.sh

The script will build the HTML documentation, checkout the Github pages branch into ``docs/_build/.build``
directory and push changes to Github.




