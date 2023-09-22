Piny
====

|Logo|

|PyPI| |Coverage| |Downloads| |License|

**Piny** is YAML config loader with environment variables interpolation for Python.

Keep your app's configuration in a YAML file.
Mark up sensitive data in the config as *environment variables*.
Set environment variables on application deployment.
Now let the *piny* load your config and substitute environment variables
in it with their values.

Piny is developed with Docker and Kubernetes in mind,
though it's not limited to any deployment system.


Rationale
---------

Piny combines *readability and versioning* you get when using config files,
and *security* that environment variables provide. Read more about this approach
in the `blog post`_.


Help
----

See `documentation`_ for more details.


Installation
------------

Just run::

  pip install -U piny


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

Piny also comes with *command line utility* that works both with files and standard
input and output:

.. code-block:: bash

  $ export PASSWORD=mySecretPassword
  $ echo "db: \${PASSWORD}" | piny
  db: mySecretPassword


Validation
----------

Piny supports *optional* data validation using third-party libraries:
`Marshmallow`_, `Pydantic`_, `Trafaret`_.

.. code-block:: python

  import marshmallow as ma
  from piny import MarshmallowValidator, StrictMatcher, YamlLoader

  class DBSchema(ma.Schema):
      login = ma.fields.String(required=True)
      password = ma.fields.String()

  class ConfigSchema(ma.Schema):
      db = ma.fields.Nested(DBSchema)

  config = YamlLoader(
      path="database.yaml",
      matcher=StrictMatcher,
      validator=MarshmallowValidator,
      schema=ConfigSchema,
  ).load(many=False)


Exceptions
----------

``LoadingError`` is thrown when something goes wrong with reading or parsing YAML-file.
``ValidationError`` is a wrapper for exceptions raised by the libraries for optional data validation.
Original exception can be accessed by ``origin`` attribute. It comes in handy when you need more than
just an original exception message (e.g. a dictionary of validation errors).

Both exceptions inherit from the ``ConfigError``.


Best practices
--------------

- Maintain a healthy security/convenience balance for your config

- Mark up entity as an environment variable in your YAML if and only if
  it really is a *secret* (login/passwords, private API keys, crypto keys,
  certificates, or maybe DB hostname too? You decide)

- When loading config file, validate your data.
  Piny supports a few popular data validation tools.

- Store your config files in the version control system along with your app’s code.

- Environment variables are set by whoever is responsible for the deployment.
  Modern orchestration systems like `Kubernetes`_ make it easier to keep envs secure
  (see `Kubernetes Secrets`_).


Fun facts
---------

*Piny* is a recursive acronym for *Piny Is Not YAML*.
Not only it's a library name, but also a name for YAML marked up
with environment variables.


Changelog
---------

See `CHANGELOG.rst`_.


Contributing
------------

See `CONTRIBUTING.rst`_.

.. |PyPI| image:: https://img.shields.io/pypi/v/piny
   :alt: PyPI
   :target: https://pypi.org/project/piny/
.. |Coverage| image:: https://img.shields.io/codecov/c/github/pilosus/piny.svg
   :alt: Codecov
   :target: https://codecov.io/gh/pilosus/piny
.. |License| image:: https://img.shields.io/github/license/pilosus/piny.svg
   :alt: MIT License
   :target: https://github.com/pilosus/piny/blob/master/LICENSE
.. |Logo| image:: https://piny.readthedocs.io/en/latest/_static/piny_logo_noborder.png
   :alt: Piny logo
   :target: https://pypi.org/project/piny/
.. |Downloads| image:: https://img.shields.io/pypi/dm/piny
   :alt: PyPI - Downloads


.. _blog post: https://blog.pilosus.org/posts/2019/06/07/application-configs-files-or-environment-variables-actually-both/?utm_source=github&utm_medium=link&utm_campaign=rationale
.. _future releases: https://github.com/pilosus/piny/issues/2
.. _Kubernetes: https://kubernetes.io/
.. _Kubernetes Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
.. _Pydantic: https://pydantic-docs.helpmanual.io/
.. _Marshmallow: https://marshmallow.readthedocs.io/
.. _Trafaret: https://trafaret.readthedocs.io/
.. _tests: https://github.com/pilosus/piny/tree/master/tests
.. _source code: https://github.com/pilosus/piny/tree/master/piny
.. _coming soon: https://github.com/pilosus/piny/issues/12
.. _CONTRIBUTING.rst: https://github.com/pilosus/piny/tree/master/CONTRIBUTING.rst
.. _CHANGELOG.rst: https://github.com/pilosus/piny/tree/master/CHANGELOG.rst
.. _documentation: https://piny.readthedocs.io/
