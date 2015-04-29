.. _topics-backends:

========
Backends
========

.. toctree::
   :maxdepth: 2

Available backends
==================

Djangoes provides only simple and basic backends: they use transport and
connection classes provided by default by ``elastichsearch-py``. They aim to
provide a set of methods easy to use, as they will automatically use the
configured indices.

ElasticSearch backends
----------------------

Each backend uses one of the connection class provided by
``elastichsearch-py``:

* ``elasticsearch.connection.http_urllib3.Urllib3HttpConnection``
* ``elasticsearch.connection.http_requests.RequestsHttpConnection``
* ``elasticsearch.connection.thrift.ThriftConnection``
* ``elasticsearch.connection.memcached.MemcachedConnection``

To configure a backend, simply add the expected keyword arguments in the
``PARAMS`` key of the connection configuration dict.

.. seealso::

   All connection classes used by these backends are describe in the
   `official documentation`__ of ``elasticsearch-py``.

   .. __: http://elasticsearch-py.readthedocs.org/en/master/transports.html

``SimpleHttpBackend``
.....................

The backend :class:`djangoes.backends.elasticsearch.SimpleHttpBackend` uses
the connection class used by default by the ``Transport`` class:
``elasticsearch.connection.http_urllib3.Urllib3HttpConnection``.

Each query will be performed with an HTTP request, using the ``urllib3``
library.

``SimpleRequestsHttpBackend``
.............................

The backend :class:`djangoes.backends.elasticsearch.SimpleRequestsHttpBackend`
uses the connection class
``elasticsearch.connection.http_requests.RequestsHttpConnection``.

Each query will be performed with an HTTP request, using the ``requests``
library (also known as `"HTTP for human"`__).

.. __: http://docs.python-requests.org/en/latest/


``SimpleThriftBackend``
.......................

The backend :class:`djangoes.backends.elasticsearch.SimpleThriftBackend`
uses the connection class ``elasticsearch.connection.thrift.ThriftConnection``.

Each query will be performed using the `Thrift`__ protocol.

.. __: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-thrift.html


``SimpleMemcachedBackend``
..........................

The backend :class:`djangoes.backends.elasticsearch.SimpleMemcachedBackend`
uses the connection class
``elasticsearch.connection.memcached.MemcachedConnection``.

Each query will be performed using `memcached`__.

.. __: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/modules-memcached.html


Custom backends
===============

Create a custom backend for your application is as easy as subclassing the
abstract class, and implement your own methods.

.. warning::

   The backend interface is not yet stable. It should be, as soon as possible,
   but not yet. So don't rush in the code without a look at the current
   available backend classes.

A backend is expected to subclass the :class:`djangoes.backends.abstracts.Base`
class. Then, its ``__init__`` method is expected to accept these three
parameters:

* ``alias``: the connection's alias. It is the key used in :data:`ES_SERVERS`
  to configure the connection using this backend.
* ``server``: the configuration dict of the connection, as found in
  :data:`ES_SERVERS`, where all undefined values are replaced by the defaults.
* ``indices``: the list of configuration dict of the connection's indices,
  as found in :data:`ES_INDICES`, where all undefined values are replaced by
  the defaults.

Extend ElasticSearch backends
-----------------------------

The built-in ``djangoes`` backends are all based on an abstract class:
:class:`djangoes.backends.elasticsearch.BaseElasticsearchBackend`. This class
conveniently subclass the abstract base class, and gives two entry point to
override its behavior:

* :attr:`~djangoes.backends.elasticsearch.BaseElasticsearchBackend.transport_class`:
  the transport class used to configure the ``elasticsearch-py`` client.
* :attr:`~djangoes.backends.elasticsearch.BaseElasticsearchBackend.connection_class`:
  the connection class used by the transport class.

If you are already familiar with the transport class and the connection classes
described in the ``elasticsearch-py`` `library documentation`__, you should not
have any issue with finding your way.

.. __: http://elasticsearch-py.readthedocs.org/en/master/transports.html
