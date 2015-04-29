.. todo::

   Explain all possible queries and their specificities. In particular, the
   get API, that can work only with a single index.

.. _topics-queries:

===============
Perform queries
===============

.. toctree::
   :maxdepth: 2

Now that you have a connection to your ElasticSearch servers, you may want to
perform queries. The connection object has an equivalent interface as the
official :py:class:`elasticsearch.client.Elasticsearch` class, but simplifies
most method by removing the ``index`` parameter.

.. seealso::

   The official `ElasticSearch API documentation`__.

.. __: http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch


Search
======

The most common query to perform is the ``search`` - which is expected for a
software named "ElasticSearch". When using djangoes, performing a search query
is as simple as using the official ``elasticsearch`` library. For example, to
perform a search query on the configured index, using the document type
"blog entry"::

   >>> from djangoes import connection
   >>> search = {'query': {'match_all': {}}}
   >>> result = connection.search(doc_type='blog_entry', body=search)
   >>> result.get('hits', {}).get('hits', [])
   [ ... list of all indexed blog entries ... ]

OK, but why the last line with the chained ``get``? Better to read both
documentations of the `search method`__, and the `search API`__ - the last
giving a sample response example::

   {
       "_shards":{
           "total" : 5,
           "successful" : 5,
           "failed" : 0
       },
       "hits":{
           "total" : 1,
           "hits" : [
               {
                   "_index" : "twitter",
                   "_type" : "tweet",
                   "_id" : "1",
                   "_source" : {
                       "user" : "kimchy",
                       "postDate" : "2009-11-15T14:12:12",
                       "message" : "trying out Elasticsearch"
                   }
               }
           ]
       }
   }

.. __: http://elasticsearch-py.readthedocs.org/en/master/api.html?highlight=search#elasticsearch.Elasticsearch.search
.. __: http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/search-request-body.html

As you can see, the response is a dict, that has a ``hits`` key, that is a dict
that also has a ``hits`` key, which is, this time, a list of documents. In fact
most of the time you will have these lines::

   >>> result_hits = results.get('hits', {})
   >>> total_count = result_hits.get('total', 0)
   >>> documents = result_hits.get('hits', [])
   >>> result_count = len(documents)

.. note::

   Yes, it might be something to work on in order to make it more "simple".
   Any idea? `Open an issue or a PR!`__

   .. __: https://github.com/exirel/djangoes


Single index operation
======================

Not all operation can be perform accross multiple indices: ``get``, ``create``
or ``update`` queries are single index operations. They can not be performed
on a list of indices, nor on an alias mapped to more than one index.

In these cases, you have two simple options:

* Use two differents connections, one for search and multi-indices queries,
  and one for single index operation.
* Use only one connection and make sure to use only one index, or an alias
  mapped to only one index.


Advanced usage
==============

To perform any advanced queries, such as getting the list of aliases for an
index, the ``client`` attribute is available on each connection: it is the
underlying client implementation.

.. warning::

   At the moment, the ``client`` attribute is not well documented as the
   behavior of the backend is supposed to change in a near future, with a more
   stable API.
