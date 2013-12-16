CouchApp: Standalone CouchDB Application Development Made Simple
================================================================
.. image:: https://travis-ci.org/couchapp/couchapp.png?branch=master
   :target: https://travis-ci.org/couchapp/couchapp

.. image:: https://coveralls.io/repos/couchapp/couchapp/badge.png
  :target: https://coveralls.io/r/couchapp/couchapp

CouchApp is designed to structure standalone CouchDB application
development for maximum application portability.

CouchApp is a set of scripts and a `jQuery <http://jquery.com>`_ plugin
designed  to bring clarity and order to the freedom of
`CouchDB <http://couchdb.apache.org>`_'s document-based approach.

Also, be sure to checkout our Erlang-based sibling,
`erica <https://github.com/benoitc/erica>`_.

Write apps using just JavaScript and HTML
-----------------------------------------

Render HTML documents using JavaScript templates run by CouchDB. You'll
get parallelism and cacheability, **using only HTML and JS.** Building
standalone CouchDB applications according to correct principles affords
you options not found on other platforms.

Deploy your apps to the client
++++++++++++++++++++++++++++++

CouchDB's replication means that programs running locally, can still be
social. Applications control replication data-flows, so publishing
messages and subscribing to other people is easy. Your users will see
the benefits of the web without the hassle of requiring always-on
connectivity.

Installation
------------

Couchapp requires Python 2.5x or sup. To install couchapp using
easy_install you must make sure you have a recent version of distribute
installed::

    $ curl -O http://python-distribute.org/distribute_setup.py
    $ sudo python distribute_setup.py
    $ easy_install pip

To install or upgrade to the latest released version of couchapp::

    $ pip install couchapp

On OSX 10.6/10.7 you may need to set ARCH_FLAGS::

    $ env ARCHFLAGS="-arch i386 -arch x86_64" pip install couchapp

To install/upgrade development version::

    $ pip install git+http://github.com/couchapp/couchapp.git#egg=Couchapp

Note: some installations need to use *sudo* command beafore each command
line.

Note on debian system don't forget to install python-dev.

To install on windows follow instructions `here
<http://www.couchapp.org/page/windows-python-installers>`_.

More installion options on the `website
<http://www.couchapp.org/page/installing>`_.

Getting started
---------------

Read the `tutorial <http://www.couchapp.org/page/getting-started>`_.

Testing
-------

We use `nose <http://nose.readthedocs.org/>`_. and
`nose-testconfig <https://pypi.python.org/pypi/nose-testconfig>`_. for setting
up and running tests.

In the ``tests`` directory, copy ``config.sample.ini`` to ``config.ini``, tweak
the settings, and then run the tests from the main ``couchapp`` directory (as
the paths below are relative to that):

    $ nosetests --tc-file=tests/config.ini

If you're wanting to generate code coverage reports (because you've got big
plans to make our tests better!), you can do so with this command instead:

    $ nosetests --with-coverage --cover-package=couchapp --cover-html --tc-file=tests/config.ini

Thanks for testing ``couchapp``!

Other resources
---------------

* `Couchapp website <http://couchapp.org>`_
* `Frequently Asked Questions <http://couchapp.org/page/faq>`_
* `couchapp command line usage <http://couchapp.org/page/couchapp-usage>`_
* `Extend couchapp command line <http://couchapp.org/page/couchapp-extend>`_
* `List of CouchApps <http://couchapp.org/page/list-of-couchapps>`_

