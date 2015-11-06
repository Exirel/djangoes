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
software named "ElasticSearch". When using ``djangoes``, performing a search
query is as simple as using the official ``elasticsearch`` library. For
example, to perform a search query on the configured index, using the document
type "blog entry"::

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

As you can see, the results is a ``dict`` that contains meta information about
the request (stats on shards), and the ``hits``, a dict that contains the
results of the query: the total number of documents that match the search
query, and the list of documents for the current page.


Single index operation
======================

Not all operation can be performed accross multiple indices: ``get``,
``create`` or ``update`` queries are single index operations. They can not be
performed on a list of indices, nor on an alias mapped to more than one index.


Advanced usage
==============

To perform any advanced queries, such as getting the list of aliases for an
index, the ``client`` attribute is available on each connection: it is the
underlying client implementation, ie. an instance of
``elasticsearch.client.Elasticsearch``.

.. warning::

   At the moment, the ``client`` attribute is not well documented as the
   behavior of the backend is supposed to change in a near future, with a more
   stable API.


Multiple connections and indices
================================

There are way too many possible configurations for your application, your
ElasticSearch servers and indices. Therefore, ``djangoes`` tries to stay
agnostic about your way of using ElasticSearch.

Let's see an example of configuration and how to use it.

.. seealso:: :doc:`configure`

Search & Single-operation configuration
---------------------------------------

In this situation, one wants to perform search queries on multiple indices,
*and* to insert documents into these indices. Let's start by the ``ES_SERVERS``
configuration::

   ES_SERVERS = {
       'default': {
           'HOSTS': ['localhost:9200'],
           'INDICES': ['categories', 'brands']
       },
       'categories': {
           'HOSTS': ['localhost:9200'],
           'INDICES': ['categories']
       },
       'brands': {
           'HOSTS': ['localhost:9200'],
           'INDICES': ['brands']
       }
   }

Now, we need to configure these indices::

   ES_INDICES = {
       'categories': {
           'SETTINGS': {
               // Category-specific index settings
           }
       },
       'brands': {
           'SETTINGS': {
               // Brand-specific index settings
           }
       }
   }

And then the magic happens::

   >>> from djangoes import connection
   >>> results = connection.search(query)
   >>> results.get('hits', {}).get('hits', [])
   [ some_category, some_brand, some_other_category, ... ]

This is possible because the ``djangoes`` client uses the
``connection.indices`` property, which is the list of aliases, or index names
if no alias is configured (which is our case here)::

   >>> connection.indices
   ['categories', 'brands']

Now, we still need to insert documents. For this, we'll use the other
connections::

   >>> from djangoes import connections
   >>> categories = connections['categories']
   >>> brands = connections['brands']
   >>> categories.create(doc_id, doc_category)
   { ... result of the create action ... }
   >>> brands.create(doc_id, doc_brand)
   { ... result of the create action ... }

As you can see, each connection has a different value for its ``indices``
attribute::

   >>> categories.indices
   ['categories']
   >>> brands.indices
   ['brands']

Therefore, you can handle this specific case - and it's only one of the many
possible solutions.

.. note::

   It's not simple to handle this case, as there are many ways to do it. At the
   moment, ``djangoes`` does not provide a really simple solution. This may
   change in a near future.
