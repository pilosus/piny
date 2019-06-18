Contributing to Piny
====================

Piny is a `proof-of-concept`_. It's developed specifically (but not
limited to!) for the containerized Python applications deployed with
orchestration systems like ``docker compose`` or ``Kubernetes``.

Piny is still in its early stage of development. The API may change,
backward compatibility between `minor versions`_ is not guaranteed until
version 1.0.0 is reached.

Piny sticks to the Unix-way's rule *Do One Thing and Do It Well*.
Piny is all about interpolating environment variables in configuration files.
Other features like YAML-parsing or data validation are implemented
using third-party libraries whenever possible.

You are welcome to contribute to *Piny* as long as you follow the rules.


General rules
-------------

1. Before writing any *code* take a look at the existing `open issues`_.
   If none of them is about the changes you want to contribute,
   open up a new issue. Fixing a typo requires no issue though,
   just submit a Pull Request.

2. If you're looking for an open issue to fix, check out
   labels `help wanted`_ and `good first issue`_ on GitHub.

3. If you plan to work on an issue open not by you, write about your
   intention in the comments *before* you start working.

4. Follow an Issue/Pull Request template.


Development rules
-----------------

1. Fork `Piny`_ on GitHub.

2. Clone your fork with ``git clone``.

3. Use ``Python 3.6+``, ``git``, ``make`` and ``virtualenv``.

4. Create and activate ``virtualenv``.

5. Install *Piny* and its dependencies with ``make install``.

6. Follow `GitHub Flow`_: create a new branch from ``master`` with
   ``git checkout -b <your-feature-branch>``. Make your changes.

7. Fix your code's formatting and imports with ``make format``.

8. Run unit-tests and linters with ``make check``.

9. Build documentation with ``make docs``.

10. Commit, push, open new Pull Request.

11. Make sure Travis CI/CD pipeline succeeds.

.. _proof-of-concept: https://blog.pilosus.org/posts/2019/06/07/application-configs-files-or-environment-variables-actually-both/
.. _minor versions: https://semver.org/
.. _open issues: https://github.com/pilosus/piny/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen
.. _help wanted: https://github.com/pilosus/piny/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22
.. _good first issue: https://github.com/pilosus/piny/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22
.. _GitHub Flow: https://guides.github.com/introduction/flow/
.. _Piny: https://github.com/pilosus/piny/fork
