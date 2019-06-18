Installation
============

Just use::

  pip install -U piny


*Piny* supports a few third-party validation libraries (see :ref:`usage-validators-docs`).
You may install *Piny* with one of them as en extra requirement::

  pip install -U 'piny[pydantic]'

The full list of extra validation libraries is the following:

- ``marshmallow``
- ``pydantic``
- ``trafaret``

You can also clone *Piny* from GitHub and install it using ``make install``
(see :ref:`contributing-docs`)::

  git clone https://github.com/pilosus/piny
  cd piny
  make install
