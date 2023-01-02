.. Piny documentation master file, created by
   sphinx-quickstart on Mon Jun 17 11:38:51 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Piny: envs interpolation for config files
=========================================

|PyPI| |Coverage| |License|

*Piny* is YAML config loader with environment variables interpolation for Python.

- Keep your app's configuration in a YAML file.
- Mark up sensitive data in config as *environment variables*.
- Set environment variables on application deployment.
- Let *Piny* load your configuration file and substitute environment variables with their values.

Piny is developed with Docker and Kubernetes in mind,
though it's not limited to any deployment system.


Simple example
--------------

Set your environment variables, mark up your configuration file with them:

.. literalinclude:: code/config.yaml
   :language: yaml

Then load your config with *Piny*:

.. literalinclude:: code/simple_yaml_loader.py


CLI utility
-----------

Piny's also got a command line tool working both with files and standard input and output:

.. code-block:: bash

  $ export PASSWORD=mySecretPassword
  $ echo "db: \${PASSWORD}" | piny
  db: mySecretPassword


Rationale
---------

Piny allows you to maintain healthy security/convenience balance
when it comes to application's configuration. Piny combines readability
and versioning you get when using config files, and security that
environment variables provide.

Read more about this approach in the `blog post`_.

.. _blog post: https://blog.pilosus.org/posts/2019/06/07/application-configs-files-or-environment-variables-actually-both/?utm_source=docs&utm_medium=link&utm_campaign=rationale


.. _user-docs:

.. toctree::
   :maxdepth: 2
   :caption: User Documentation

   install
   usage
   integration
   best

.. _dev-docs:

.. toctree::
   :maxdepth: 2
   :caption: Developer Documentation

   contributing
   changelog

.. _misc-docs:

.. toctree::
   :maxdepth: 2
   :caption: Misc

   misc

.. |PyPI| image:: https://img.shields.io/pypi/v/piny
   :alt: PyPI
   :target: https://pypi.org/project/piny/
.. |Coverage| image:: https://img.shields.io/codecov/c/github/pilosus/piny.svg
   :alt: Codecov
   :target: https://codecov.io/gh/pilosus/piny
.. |License| image:: https://img.shields.io/github/license/pilosus/piny.svg
   :alt: MIT License
   :target: https://github.com/pilosus/piny/blob/master/LICENSE
