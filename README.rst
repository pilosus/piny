|Build| |Maintainability| |Coverage| |Black| |Versions| |License|

Piny
====

YAML configs loader with environment variables interpolation for Python.

Keep your app's configuration in YAML file with sensitive data marked as environment variables.
Put sensitive data into environment variables. Then let *piny* interpolate
the variables on YAML loading.

Rationale
---------

Piny combines YAML config's readability, versioning, and environment variable's security.
Read more in the `blog post`_.


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


Best practices
--------------

  - Maintain healthy security/convenience balance for your config

  - Mark up entity as an environment variable in your YAML if and only if
    it really is a *secret* (login/passwords, private API keys, crypto keys,
    certificates, or maybe DB hostname too? You decide)

  - Once config is loaded by Piny validate it using your favourite validation tool
    (some integrations are coming in the `future releases`_)

  - Store your config files in the version control system along with you app’s code.

  - Environment variables are set by whomever is responsible for the deployment.
    Modern orchestration systems like `Kubernetes`_ make it easier to keep envs secure
    (see `Kubernetes Secrets`_).

Fun facts
---------

*Piny* is a recursive acronym for *Piny Is Not YAML*.
Not only it's a library name, but also a name for YAML marked up
with environment variables.


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
.. _blog post: https://blog.pilosus.org/posts/2019/06/07/application-configs-files-or-environment-variables-actually-both/?utm_source=github&utm_medium=link&utm_campaign=rationale
.. _future releases: https://github.com/pilosus/piny/issues/2
.. _Kubernetes: https://kubernetes.io/
.. _Kubernetes Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
