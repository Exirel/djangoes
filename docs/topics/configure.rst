.. _topics-confugure:

=============================
Configure your django project
=============================

.. toctree::
   :maxdepth: 2

After installing ``djangoes``, you need to configure your django project
settings with two variables:

* ``ES_SERVERS``: configure connections to ElasticSearch servers,
* ``ES_INDICES``: configure ElasticSearch indices used by connections.

The main idea behind this separation is to configure the connections, the way
to access the ElasticSearch API, and the indices separatly, where the documents
are stored and how to access to them, then to decide what indices each
connection will use.

For example, you can have two connections, one for each host, and both use the
same index configuration.

Connection configuration
========================

The setting ``ES_SERVERS`` is a dict, where each key is a connection
configuration alias (its name), and each value is a dict that describes one
connection. By default, there is one connection named ``default`` - the same
way there is a ``default`` database connection alias in Django.

The keys expected in a connection dict are:

* ``HOSTS``: a hosts configuration, as expected by `elasticsearch-py`_,
* ``ENGINE``: a string giving the class path to the engine backend class,
* ``INDICES``: a ``list`` of index alias as found in ``ES_INDICES``,
* ``PARAMS``: a ``dict`` used as keyword arguments to instanciate the backend
  class.

.. _elasticsearch-py: https://pypi.python.org/pypi/elasticsearch

Example::

   ES_SERVERS = {
       'default': {
           'HOSTS': ['es_host_1', 'es_host_2'],
           'ENGINE': 'djangoes.backends.elasticsearch.SimpleHttpClient',
           'INDICES': ['index_1']
       }
   }

Index configuration
===================

The setting ``ES_INDICES`` is a dict, where each key is an index configuration
alias (its name as used by connections in ``ES_SERVERS`` in their ``INDICES``
option), and each value is a dict that describes one index. By default, there
is not any index configured.

The keys expected in an index dict are:

* ``NAME``: a ``string``, its index name, by default it will be its
  configuration alias if not explicitly given,
* ``ALIASES``: a ``list`` of alias names, by default an empty ``list``,
* ``TESTS``: a ``dict`` used to configure index when testing.

Example::

   ES_INDICES = {
       'index_1': {
           'NAME': 'real_index_name',
           'ALIASES': ['index_catalog', 'index_public'],
       }
   }
