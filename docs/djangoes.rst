=====================
Package documentation
=====================

.. automodule:: djangoes

.. toctree::
   :maxdepth: 2

   djangoes/test


.. py:data:: connections

   Module-level attribute, instance of :class:`ConnectionHandler`.

   It can be considered as a singleton: it is the default connections handler
   to use with :mod:`djangoes`. It is instantiated at import with the default
   arguments.

   Therefore, this object will automatically use the settings of your
   django project: :data:`ES_SERVERS` and :data:`ES_INDICES`.


.. autoclass:: ConnectionHandler
   :members:
