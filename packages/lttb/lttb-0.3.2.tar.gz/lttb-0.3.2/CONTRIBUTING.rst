Contributing
============

Reporting issues
----------------

If you find a bug or have an idea for improving this package,
please describe it in a message to the |mailinglist|.

.. |mailinglist| replace:: `mailing list <https://lists.sr.ht/~javiljoen/lttb-devel>`__


Submitting patches
------------------

Patches are welcome.
Feel free to send them to |mailinglist| using ``git send-email``,
or you can send me a link to your repo if it is publicly accessible.
If you prefer the pull request workflow,
you can also send me a PR at https://codeberg.org/javiljoen/lttb-numpy.

Please ensure that the tests and linting checks listed in the ``Makefile`` all pass,
and that any new features are covered by tests.


Development setup
-----------------

Create a Python virtual environment, e.g. using ``python3 -m venv``.
In that venv, install the dependencies and development tools::

   pip install -e .[test,dev]

The linters and tests can then be run with the commands in the ``Makefile``::

   make lint
   make test
