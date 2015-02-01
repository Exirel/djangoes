======================
Djangoes documentation
======================

.. toctree::
   :maxdepth: 2

   topics/connections
   topics/queries
   topics/configure
   djangoes

.. warning::

   This project is not production-ready yet, and it's published as Alpha
   version on Pypi. It works, it can be used, but its internal and public
   interfaces are not stable yet, and may change in a near future without
   warnings.

   As soon as the application is considered stable, this warning will be
   removed and the package published on Pypi will be marked as beta, then
   stable/production ready.

   Deprecration warnings will be used, and a release cycle will be exposed,
   with all the version management we all wish to have.


Install
=======

To install ``djangoes`` and its dependencies, the simple way is to use pip::

   $ pip install djangoes django elasticsearch

You should always use ``pip`` to install ``djangoes``.

You will also need an ElasticSearch server. See the official documentation
for that, but if you are running on Debian or Ubuntu, it will be as simple
as adding a repository to your sources list and shoot an ``apt-get install``
in your favorite shell.

Short introduction
==================

When you have installed ``djangoes``, you can configure your Django project
with two news settings, like this::

   # in your settings file
   ES_SERVERS = {
       'default': {
           'HOSTS': ['localhost', ],
           'INDICES': ['my_index'],
       }
   }

   ES_INDICES = {
       'my_index': {
           'NAME': 'index_dev',
       }
   }

.. seealso::

   The :doc:`topics/configure` chapter explains how to configure the
   connections to ElasticSearch in your Django project using ``djangoes``.

Then you can build your first view and use :data:`djangoes.connection` to
query ElasticSearch::

   # in a views.py
   from django.shortcuts import render
   from djangoes import connection


   def search_blog_entries(request):
       search_term = request.GET['q']
       query = {
           'query': {
               'match': {
                   'text': search_term
               }
           }
       }
       result = connection.search(doc_type='entry', body=query)
       return render(request, 'search/results.html', {'results': result})

.. seealso::

   The :doc:`topics/connections` and :doc:`topics/queries` chapters explain
   how to get a connection and how to perform queries.


And finally in your template, you can display the result with this::

   <h1>Blog post found</h1>

   {% for hit in results.hits.hits %}
       <article>
           <h2>{{hit._source.title}}</h2>
           {{hit._source.text}}
       </article>
   {% endfor %}

Note that this example uses the raw result, without any specific modification.
It's because ``djangoes`` provides the connection layer only - everything else
remains up to the developer to decide (for example by using the official DSL
library, named `elasticsearch-dsl`__).


.. __: http://elasticsearch-dsl.readthedocs.org/en/latest/

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
