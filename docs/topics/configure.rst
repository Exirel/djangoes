.. _topics-confugure:

=============================
Configure your django project
=============================

.. toctree::
   :maxdepth: 2

After installing :mod:`djangoes`, you need to configure your django project
settings with two variables:

* :data:`ES_SERVERS`: configure connections to ElasticSearch servers,
* :data:`ES_INDICES`: configure ElasticSearch indices used by connections.

The main idea behind this separation is to configure the connections, the way
to access the ElasticSearch API, and the indices separatly, where the documents
are stored and how to access to them, then to decide what indices each
connection will use.

For example, you can have two connections, one for each host, and both use the
same index configuration.

Settings
========

.. py:data:: ES_SERVERS

   The setting ``ES_SERVERS`` is a dict, where each key is a connection
   configuration alias (its name), and each value is a dict that describes one
   connection. By default, there is one connection named ``default`` - the same
   way there is a ``default`` database connection alias in Django.

   The keys expected in a connection dict are:

   * ``HOSTS``: a hosts configuration, as expected by `elasticsearch-py`_,
   * ``ENGINE``: a string giving the class path to the engine backend class,
   * ``INDICES``: a ``list`` of index alias as found in ``ES_INDICES``,
   * ``PARAMS``: a ``dict`` used as keyword arguments to instanciate the
     backend class.

   .. _elasticsearch-py: https://pypi.python.org/pypi/elasticsearch

   Example::

      ES_SERVERS = {
          'default': {
              'HOSTS': ['es_host_1', 'es_host_2'],
              'ENGINE': 'djangoes.backends.elasticsearch.SimpleHttpClient',
              'INDICES': ['index_1']
          }
      }

   .. seealso:: :doc:`backends`

      The :doc:`backends` chapter gives more information about the available
      backends, how they work and how to build yours.


.. py:data:: ES_INDICES

   The setting ``ES_INDICES`` is a dict, where each key is an index
   configuration alias (its name as used by connections in :data:`ES_SERVERS`
   in their ``INDICES`` option), and each value is a dict that describes one
   index. By default, no index are defined.

   The expected keys are:

   * ``NAME``: a ``string``, its index name, by default it will be its
     configuration alias if not explicitly given,
   * ``ALIASES``: a ``list`` of alias names, by default an empty ``list``,
   * ``SETTINGS``: an optionnal ``dict`` used to describe the index's settings
     when creating this index.
   * ``TESTS``: a ``dict`` used to configure index when testing.

   Example::

      ES_INDICES = {
          'index_1': {
              'NAME': 'real_index_name',
              'ALIASES': ['index_catalog', 'index_public'],
          }
      }

The ``SETTINGS`` parameter
--------------------------

Each index can have its own configuration: analyzers, tokenizers, and other
index-specific settings. ``djangoes`` uses these settings in its test-case
methods to create the test indices.

You might also use it in your own code thanks to the
:meth:`~djangoes.backends.abstracts.Base.get_indices_with_settings` method::

   >>> indices_with_settings = connection.get_server_indices()
   >>> for index_name, settings_body in indices_with_settings.items():
   ...     connection.client.indices.create(index_name, settings_body)


Timeout and retry on error
==========================

Timeout configuration and management can be very important for your
application, and it can become complicated to understand which parameters are
available, and what they exactly mean - thus how to configure them.

As djangoes uses the official ElasticSearch python library to implement its
client engines, it allows to configure the behavior on error caused by timeout:
should the client retry on another server on timeout or not? How long a server
should be marked as dead after a timeout? How many time should the client
retry after an error?

In :data:`ES_SERVERS`, each connection has a ``PARAMS`` key that contains the
keyword arguments that will be given to the ``ENGINE`` backend class. Some of
these arguments, described below, allow to control the behavior after a timeout
or a connection error.

.. describe:: max_retries

   Maximum number of retry after an error before a request raise an error.

   It means that, when performing a request, the client will try as many time
   as ``max_retries`` before it raises an error.

   It won't retry on client error, such as invalid request, but it will retry
   on another host if one is not reachable.

   By default, it does not retry after a timeout error.


.. describe:: timeout

   The time (in seconds) until a request to a server raises a timeout error.


.. describe:: retry_on_timeout

   Indicates if the client must retry after a timeout or not. By default the
   client won't retry after a timeout, and will raise directly.


.. describe:: dead_timeout

   Number of seconds a connection should be retired for after a failure,
   increases on consecutive failures


.. describe:: timeout_cutoff

   Number of consecutive failures after which the timeout doesn’t increase.


Example::

   ES_SERVERS = {
       'default': {
           'HOSTS': ['host_1', 'host_2']
           'PARAMS': {
               'timeout': 1,
               'retry_on_timeout': True,
               'max_retries': 3
           }
       }
   }

In this example, a request will raise a timeout error after 1 second, but the
client will retry at most 3 times before raising a connection error itself.

.. seealso::

   ElasticSearch `Transport documentation`__ gives information about the
   behavior after an error (retry or not), and the
   `ConnectionPool documentation`__ gives information about timeout
   configuration.

.. __: http://elasticsearch-py.readthedocs.org/en/master/connection.html#elasticsearch.Transport
.. __: http://elasticsearch-py.readthedocs.org/en/master/connection.html#elasticsearch.ConnectionPool
