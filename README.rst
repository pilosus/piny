|Build| |Maintainability| |Coverage| |Black| |Versions| |License|

Piny
====

YAML configs loader with environment variables interpolation for Python.

Keep your app's configuration in YAML file with sensitive data marked as environment variables.
Put sensitive data into environment variables. Then let *piny* interpolate
the variables on YAML loading.

*Piny* is a recursive acronym for *Piny Is Not YAML*


Installation
------------

Install using ``pip install -U piny``.


Usage
-----

Set your environment variables, add them to your YAML configuration file:

.. code-block:: yaml

    db:
      login: user
      password: ${DB_PASSWORD}
    mail:
      login: user
      password: ${MAIL_PASSWORD:-my_default_password}
    sentry:
      dsn: ${VAR_NOT_SET}

Then load your config:

.. code-block:: python

    from piny import YamlLoader

    config = YamlLoader(path="config.yaml").load()
    print(config)
    # {'db': {'login': 'user', 'password': 'my_db_password'},
    # 'mail': {'login': 'user', 'password': 'my_default_password'},
    # 'sentry': {'dsn': None}}

You may want to discourage Bash-style envs with defaults in your configs.
In such case, use a ``StrictMatcher``:

.. code-block:: python

    from piny import YamlLoader, StrictMatcher

    config = YamlLoader(path="config.yaml", matcher=StrictMatcher).load()

Both strict and default matchers produce ``None`` value if environment variable
matched is not set in the system (and no default syntax used in the case of
default matcher).


.. |Build| image:: https://travis-ci.org/pilosus/piny.svg?branch=master
   :target: https://travis-ci.org/pilosus/piny
.. |Maintainability| image:: https://img.shields.io/codeclimate/maintainability/pilosus/piny.svg
   :target: https://travis-ci.org/pilosus/piny
   :alt: Code Climate maintainability
.. |Coverage| image:: https://img.shields.io/codeclimate/coverage/pilosus/piny.svg
   :target: https://codeclimate.com/github/pilosus/piny/test_coverage
   :alt: Code Climate coverage
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Black Formatter
.. |Versions| image:: https://img.shields.io/pypi/pyversions/piny.svg
   :alt: PyPI - Python Version
   :target: https://pypi.org/project/piny/
.. |License| image:: https://img.shields.io/github/license/pilosus/piny.svg
   :alt: MIT License
   :target: https://github.com/pilosus/piny/blob/master/LICENSE
