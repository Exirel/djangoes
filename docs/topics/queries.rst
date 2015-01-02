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

For example, to perform a search query on the configured index, using the
document type "blog entry"::

   >>> from djangoes import connection
   >>> search = {'query': {'match_all': {}}}
   >>> result = connection.search(doc_type='blog_entry', body=search)
   >>> result.get('hits', {}).get('hits', [])
   [ ... list of all indexed blog entries ... ]

.. seealso::

   The official `ElasticSearch API documentation`__.

.. __: http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch
