.. _topics-connections:

============================
Connections to ElasticSearch
============================

.. toctree::
   :maxdepth: 2

The :mod:`djangoes` package provides a simple way to use and to access the
default connection to your ElasticSearch server. In any of your python file of
your Django project, simply import :obj:`~djangoes.connection` like this::

   from djangoes import connection

Then in any function or method you need to perform a query, you can use the
methods from the ElasticSearch python library by using this ``connection``
object::

   def search_blog_entries(words):
       """Search for all blog entries with ``words`` found in entry body."""
       doc_type = 'entry'
       search = {
           'query': {
               'term': {
                   'text': words
               }
           }
       }
       result = connection.search(doc_type, search)

       # Result from ES "as is", not modified by djangoes.
       return result.get('hits', {}).get('hits', [])

If you want to select a specific connection, you can import
:obj:`~djangoes.connections` instead::

   from djangoes import connections

And it can be used like this::

   # in some function or method
   conn = connections['connection_alias']

In fact, the :obj:`~djangoes.connection` object is a simple proxy to the
default connection, simply named ``default``::

   >>> from djangoes import connection, connections
   >>> connection == connections['default']
   True


Threading and multiprocessing
=============================

Using ``connection`` or ``connections`` is **thread-safe**, but you should
never use a connection object itself in multiple threads. If you need to
"share" a connection from one thread to another, simply use its alias and get
it using ``connections[alias]`` into the threaded code.

The same way, you shoulw **never** share a connection object between multiple
process (either with multiprocessing or forking), and instead use the
``connection`` shortcut or ``connections[alias]`` to get any connection.

Connection's methods are not thread or multi-process safe by themselves, and an
unappropriate usage may end in unexpected behavior.
