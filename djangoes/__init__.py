"""Djangoes package aims to provide a simple way to integrate ElasticSearch.

This package mimics the behavior of the Django database configuration layer,
using project settings and a global connections handler.

The simplest way to use ``djangoes`` is to import ``djangoes.connections`` and
to perform queries with it::

   >>> from djangoes import connections
   >>> conn = connections['conn_name']
   >>> result = conn.search(...)

When a connection is requested in the application for the first time, the
connection handler will build a new connection, ensuring default and tests
values.

There is a shortcut to get the default connection::

   >>> from djangoes import connection, connections
   >>> connection == connections['default']
   True
   >>> result = connection.search(...)

It works exactly like getting the ``default`` connection from ``connections``.

.. note::

    This module is based on the ``django.db`` module, which is quite simple in
    its way to deal with connections. The ``djangoes`` package hope to stay as
    simple as possible for everyone, and to take benefit from the hard works
    that make Django a great framework.

.. seealso::

    The :mod:`djangoes.handlers.connections` module contains the class used to
    handle connections configuration and access.

"""
from .handlers.connections import ConnectionHandler, DEFAULT_CONNECTION_ALIAS
from .handlers.indices import IndexHandler, DEFAULT_INDEX_ALIAS

__version__ = '0.3.0'


#: Global indices handler for ``djangoes``.
indices = IndexHandler(ConnectionHandler())


#: Global connections handler for ``djangoes``.
#: One can import ``djangoes.connections`` and ask for a connection that will
#: be thread safe and configured through the project settings.
connections = indices.connections  #pylint: disable=invalid-name


class ConnectionProxy(object):
    """Proxy for the default ``ConnectionWrapper``'s attributes.

    This class is based on ``django.db.DefaultConnectionProxy`` used for the
    default database.
    """
    def __init__(self, alias):
        self.__dict__['alias'] = alias or DEFAULT_CONNECTION_ALIAS

    def __getattr__(self, item):
        return getattr(connections[self.__dict__['alias']], item)

    def __setattr__(self, name, value):
        return setattr(connections[self.__dict__['alias']], name, value)

    def __delattr__(self, name):
        return delattr(connections[self.__dict__['alias']], name)

    def __eq__(self, other):
        return connections[self.__dict__['alias']] == other

    def __ne__(self, other):
        return connections[self.__dict__['alias']] != other


#: Default connection to ElasticSearch.
#: This is equivalent to call ``djangoes.connections['default']``.
connection = ConnectionProxy(  #pylint: disable=invalid-name
    DEFAULT_CONNECTION_ALIAS)
