Installing h in a development environment
=========================================

The code for the https://hypothes.is/ web service and API lives in a
`Git repo named h`_. This page will walk you through getting this code running
in a local development environment.

.. seealso::

   This page documents how to setup a development install of h.
   For installing the Hypothesis client for development see
   https://github.com/hypothesis/client/, and for the browser extension
   see https://github.com/hypothesis/browser-extension.

   To get "direct" or "in context" links working you need to install Bouncer
   and Via. See https://github.com/hypothesis/bouncer and
   https://github.com/hypothesis/via.

You will need
-------------

Before installing your local development environment you'll need to install
each of these prerequisites:

* `Git <https://git-scm.com/>`_

* `Node <https://nodejs.org/>`_ and npm.
  On Linux you should follow
  `nodejs.org's instructions for installing node <https://nodejs.org/en/download/package-manager/>`_
  because the version of node in the standard Ubuntu package repositories is
  too old.
  On macOS you should use `Homebrew <https://brew.sh/>`_ to install node.

* `Gulp <https://gulpjs.com/>`_.
  Once you have npm you can just run ``sudo npm install -g gulp-cli`` to install ``gulp``.

* `Docker CE <https://docs.docker.com/install/>`_ and `Docker Compose <https://docs.docker.com/compose/>`_.
  Follow the `instructions on the Docker website <https://docs.docker.com/compose/install/>`_
  to install these.


* `pyenv`_.
  Follow the instructions in the pyenv README to install it.

Clone the Git repo
------------------

.. code-block:: shell

   git clone https://github.com/hypothesis/h.git

This will download the code into an ``h`` directory in your current working
directory. You need to be in the ``h`` directory from the remainder of the
installation process:

.. code-block:: shell

   cd h

Run the services with Docker Compose
------------------------------------

Install and run the services the h requires using Docker Compose:

.. code-block:: shell

   docker-compose up

You'll now have some Docker containers running the PostgreSQL, RabbitMQ, and
Elasticsearch services. You should be able to see them by running ``docker
ps``. You should also be able to visit your Elasticsearch service by opening
http://localhost:9200/ in a browser, and connect to your PostgreSQL by
running ``psql postgresql://postgres@localhost/postgres`` (if you have psql
installed).

Use pyenv to install Python and tox
-----------------------------------

`pyenv`_ installs versions of Python in a ``~/.pyenv`` directory in your home
directory. It lets you have multiple versions of Python installed at once and
easily switch between them. This is much easier and safer than using your
system Python.

Install Python 2.7 and 3.6 in pyenv and install tox in each:

.. code-block:: shell

   pyenv install 2.7.16
   pyenv install 3.6.8
   pyenv shell 2.7.16
   pip install tox>=3.8.0
   pyenv shell 3.6.9
   pip install tox>=3.8.0
   pyenv shell --unset

Start the development server
----------------------------

.. code-block:: shell

    make dev

The first time you run ``make dev`` it might take a while to start because
it'll need to install the application dependencies and build the client assets.

This will start the server on port 5000 (http://localhost:5000), reload the
application whenever changes are made to the source code, and restart it should
it crash for some reason.

Create the ``htest`` database
------------------------------

To be able to run the tests you need to create the ``htest`` database in the
``postgres`` container:

.. code-block:: shell

   docker-compose exec postgres psql -U postgres -c "CREATE DATABASE htest;"

.. _running-the-tests:

Running the tests, linters and code formatters
----------------------------------------------

To run the unit tests (both backend and frontend) run:

.. code-block:: shell

   make test

To run the functional tests:

.. code-block:: shell

   make functests

To format your code correctly:

.. code-block:: shell

   make format

To run the linter:

.. code-block:: shell

   make lint

For many more useful ``make`` commands see:

.. code-block:: shell

   make help

Running the backend tests only
##############################

To run the backend test suite only call ``tox`` directly. For example:

.. code-block:: shell

   # Run the backend unit tests:
   tox

   # Run the backend unit tests in Python 3:
   tox -e py36-tests

   # Run the backend functional tests:
   tox -e py27-functests
   tox -e py36-functests

   # Run only one test directory or test file:
   tox tests/h/models/annotation_test.py
   tox -e py36-tests tests/h/models/annotation_test.py
   tox -e py27-functests tests/functional/api/test_profile.py
   tox -e py36-functests tests/functional/api/test_profile.py

   # To pass arguments to pytest put them after a `--`:
   tox -- --exitfirst --pdb --failed-first tests/h
   tox -e pyXY-FOO -- --exitfirst --pdb --failed-first tests/h

   # See all of pytest's command line options:
   tox -- -h

Running the frontend tests only
###############################

To run the frontend test suite only, run the appropriate test task with gulp.
For example:

.. code-block:: shell

    gulp test

When working on the front-end code, you can run the Karma test runner in
auto-watch mode which will re-run the tests whenever a change is made to the
source code. To start the test runner in auto-watch mode, run:

.. code-block:: shell

    gulp test-watch

To run only a subset of tests for front-end code, use the ``--grep``
argument or mocha's `.only()`_ modifier.

.. code-block:: shell

    gulp test-watch --grep <pattern>

.. _.only(): http://jaketrent.com/post/run-single-mocha-test/

SQL query logging
-----------------

You can turn on SQL query logging by setting the ``DEBUG_QUERY``
environment variable (to any value). Set it to the special value ``trace`` to
turn on result set logging as well.

Feature flags
-------------

Features flags allow admins to enable or disable features for certain groups
of users. You can enable or disable them from the Administration Dashboard.

To access the Administration Dashboard, you will need to first create a
user account in your local instance of H and then give that account
admin access rights using H's command-line tools.

See the :doc:`/developing/administration` documentation for information
on how to give the initial user admin rights and access the Administration
Dashboard.

Troubleshooting
---------------

Cannot connect to the Docker daemon
###################################

If you get an error that looks like this when trying to run ``docker``
commands::

 Cannot connect to the Docker daemon. Is the docker daemon running on this host?
 Error: failed to start containers: postgres

it could be because you don't have permission to access the Unix socket that
the docker daemon is bound to. On some operating systems (e.g. Linux) you need
to either:

* Take additional steps during Docker installation to give your Unix user
  access to the Docker daemon's port (consult the installation
  instructions for your operating system on the Docker website), or

* Prefix all ``docker`` and ``docker-compose`` commands with ``sudo``.


.. _Git repo named h: https://github.com/hypothesis/h/
.. _pyenv: https://github.com/pyenv/pyenv
