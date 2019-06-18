Best practices
==============

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

.. _Kubernetes: https://kubernetes.io/
.. _Kubernetes Secrets: https://kubernetes.io/docs/concepts/configuration/secret/
