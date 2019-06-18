Usage
=====

*Piny* loads your YAML configuration file. It optionally validates
data loaded from config file. *Piny* main logic is in a loader class.
You can pass arguments in the loader class to change the way YAML file
is parsed and validated.

.. _usage-loaders-docs:

Loaders
-------

As for now, *Piny* supports the only loader class called ``YamlLoader``.
Based on `PyYAML`_, it parses YAML files, (arguably) the most beautiful
file format for configuration files!

Basic loader usage is the following.

1. Set your environment variables

2. Mark up your YAML configuration file with these env names:

.. literalinclude:: code/config.yaml
   :language: yaml

3. In your app load config with *Piny*:

.. literalinclude:: code/simple_yaml_loader.py

.. automodule:: piny.loaders
    :members:
    :undoc-members:
    :show-inheritance:

.. _PyYAML: https://pypi.org/project/PyYAML/

.. _usage-matchers-docs:

Matchers
--------

In the :ref:`usage-loaders-docs` section we used Bash-style environment
variables with defaults. You may want to discourage such envs in
your project. This is where *matchers* come in handy. They apply a
regular expression when parsing your YAML file that matches environment
variables we want to interpolate.

By default ``MatcherWithDefaults`` is used. ``StrictMatcher`` is another
matcher class used for plain vanilla envs with no default values support.

Both strict and default matchers return ``None`` value if environment variable
matched is not set in the system.

Basic usage example is the following:

.. literalinclude:: code/strict_matcher.py

.. automodule:: piny.matchers
    :members:
    :undoc-members:
    :show-inheritance:


.. _usage-validators-docs:

Validators
----------

Piny supports *optional* data validation using third-party libraries:
`Marshmallow`_, `Pydantic`_, `Trafaret`_.

In order to use data validation pass ``validator`` and ``schema`` arguments
in the :ref:`usage-loaders-docs` class. You may also initialize loader class
with optional named arguments that will be passed to the validator's schema.
Additional loading arguments may be passed in ``load`` method invocation.

.. automodule:: piny.validators
    :members:
    :undoc-members:
    :show-inheritance:


Marshmallow validation example
..............................

.. literalinclude:: code/ma_validation.py


Pydantic validation example
...........................

.. literalinclude:: code/pydantic_validation.py


Trafaret validation example
...........................

.. literalinclude:: code/trafaret_validation.py

.. _Pydantic: https://pydantic-docs.helpmanual.io/
.. _Marshmallow: https://marshmallow.readthedocs.io/
.. _Trafaret: https://trafaret.readthedocs.io/

.. _usage-exceptions-docs:

Exceptions
----------

``LoadingError`` is thrown when something goes wrong with reading or
parsing a YAML file. ``ValidationError`` is a wrapper for exceptions
raised by the libraries for optional data validation. Original exception
can be accessed by ``origin`` attribute. It comes in handy when you need
more than just an original exception message (e.g. a dictionary of validation
errors).

Both exceptions inherit from the ``ConfigError``.

.. automodule:: piny.errors
    :members:
    :undoc-members:
    :show-inheritance:
