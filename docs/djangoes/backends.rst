========
backends
========

.. automodule:: djangoes.backends

backends.abstracts
==================

.. automodule:: djangoes.backends.abstracts

.. autoclass:: djangoes.backends.abstracts.Base
   :members:

   .. attribute:: indices

      List of names to use to perform ElasticSearch queries.

      For each configured index, a connection will use either its index name,
      or its list of aliases if at least one is defined.

      For example, if a connection uses 2 indices, one with only the ``index``
      index, and the second one with the ``index_2`` index and an alias
      `̀ alias``, the result `̀ indices`` will be ``['index', 'alias']``.

   .. attribute:: index_names

      List of names of all configured indices, without their aliases.

      It is the same list of :attr:`indices` but where indices are not replaced
      by their aliases.

      It is particulary useful when indices need to be created for example.

   .. attribute:: alias_names

      List of names of all configured indices's aliases, without their indices.

      It is the same list of :attr:`indices` but where only aliases are
      presents.

      It is particulary useful when aliases need to be created for example.


.. autoclass:: djangoes.backends.abstracts.MetaClientBase
   :members:


backends.elasticsearch
======================

.. automodule:: djangoes.backends.elasticsearch
   :members:

.. autoclass:: djangoes.backends.elasticsearch.SimpleHttpBackend
   :members:
