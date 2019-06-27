Integration Examples
====================

Flask
-----

`Flask`_ is a microframework for Python web applications. It's flexible and extensible.
Although there are best practices and traditions, Flask doesn't really enforce
the only one way to do it.

If you are working on a small project the chances are that you are using some Flask
extensions like `Flask-Mail`_ or `Flask-WTF`_. The extensions of the past are often
got configured through environment variables only. It makes the use of *Piny* cumbersome.
In mid-sized and large Flask projects though, you usually avoid using extra dependencies
whenever possible. In such a case you can fit your code to use *Piny* pretty easy.

Here is an example of a simple Flask application. Configuration file is loaded with *Piny*
and validated with *Pydantic*.

.. literalinclude:: code/flask_integration.py

You can use the same pattern with application factory in other frameworks,
like `aiohttp`_ or `sanic`_.

.. _Flask: http://flask.pocoo.org/docs/1.0/
.. _Flask-Mail: https://pythonhosted.org/Flask-Mail/
.. _Flask-WTF: https://flask-wtf.readthedocs.io/en/stable/
.. _aiohttp: https://aiohttp.readthedocs.io/en/stable/
.. _sanic: https://sanic.readthedocs.io/en/latest/


Command line
------------

There are many possible applications for *Piny* CLI utility.
For example, you can use it for `Kubernetes deployment automation`_
in your CI/CD pipeline.

Piny command line tool works both with standard input/output and files.


Standard input and output
.........................

.. code-block:: bash

  $ export PASSWORD=mySecretPassword
  $ echo "db: \${PASSWORD}" | piny
  db: mySecretPassword


Files
.....


.. code-block:: bash

  $ piny config.template config.yaml


Or you can substitute environment variables in place:

.. code-block:: bash

  $ piny production.yaml production.yaml


.. _Kubernetes deployment automation: https://www.digitalocean.com/community/tutorials/how-to-automate-deployments-to-digitalocean-kubernetes-with-circleci