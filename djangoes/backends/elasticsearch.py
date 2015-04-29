"""Connection backends based on the elasticsearch official python library.

This module aims to contain only basic backend classes using the ElasticSearch
official python library and its basics transport classes with few changes.

Each backend implements the expected behavior defined in the base class - that
is to say: they provide methods that don't need to get an index or an alias
as argument to perform requests (when applicable).
"""
from django.core.exceptions import ImproperlyConfigured
from elasticsearch.client import Elasticsearch, Transport
from elasticsearch.connection.http_urllib3 import Urllib3HttpConnection
from elasticsearch.connection.http_requests import RequestsHttpConnection
from elasticsearch.connection.thrift import ThriftConnection
from elasticsearch.connection.memcached import MemcachedConnection

from .abstracts import Base


class BaseElasticsearchBackend(Base):
    """Base connection wrapper based on the ElasticSearch official library.

    It uses two entry points to configure the underlying connection:

    * ``transport_class``: the transport class from ``elasticsearch``. By
      default ``elasticsearch.transport.Transport``.
    * ``connection_class``: the connection class used by the transport class.
      It's undefined by default, as it is on the subclasses to provide one.

    If any of these elements is not defined, an ``ImproperlyConfigured`` error
    will be raised when the backend will try to configure the client.
    """
    #: ElasticSearch transport class used by the client class to perform
    #: requests.
    transport_class = Transport
    #: ElasticSearch connection class used by the transport class to perform
    #: requests.
    connection_class = None

    def configure_client(self):
        """Instantiate and configure the ElasticSearch client.

        It simply takes the given HOSTS list and uses PARAMS as the keyword
        arguments of the ElasticSearch class.

        The client's transport_class is given by the class attribute
        ``transport_class``, and the connection class used by the transport
        class is given by the class attribute ``connection_class``.

        An ``ImproperlyConfigured`` exception is raised if any of these
        elements is undefined.
        """
        hosts = self.server['HOSTS']
        params = self.server['PARAMS']

        if not self.transport_class:
            raise ImproperlyConfigured(
                'Djangoes backend %r is not properly configured: '
                'no transport class provided' % self.__class__)

        if not self.connection_class:
            raise ImproperlyConfigured(
                'Djangoes backend %r is not properly configured: '
                'no connection class provided' % self.__class__)

        #pylint: disable=star-args
        self.client = Elasticsearch(hosts,
                                    transport_class=self.transport_class,
                                    connection_class=self.connection_class,
                                    **params)

    # Server methods
    # ==============
    # The underlying client does not require index names to perform server
    # related queries, such as "ping" or "info". The connection wrapper act
    # for them as a proxy.

    def ping(self, **kwargs):
        return self.client.ping(**kwargs)

    def info(self, **kwargs):
        return self.client.info(**kwargs)

    def put_script(self, lang, script_id, body, **kwargs):
        return self.client.put_script(lang, script_id, body, **kwargs)

    def get_script(self, lang, script_id, **kwargs):
        return self.client.get_script(lang, script_id, **kwargs)

    def delete_script(self, lang, script_id, **kwargs):
        return self.client.delete_script(lang, script_id, **kwargs)

    def put_template(self, template_id, body, **kwargs):
        return self.client.put_template(template_id, body, **kwargs)

    def get_template(self, template_id, body=None, **kwargs):
        return self.client.get_template(template_id, body, **kwargs)

    def delete_template(self, template_id=None, **kwargs):
        return self.client.delete_template(template_id, **kwargs)

    # Bulk methods
    # ============
    # The underlying client does not require index names, but it can be used.
    # As it makes sense to not give an index, developers are free to use these
    # as they want, as long as they are careful.

    def mget(self, body, index=None, doc_type=None, **kwargs):
        return self.client.mget(body, index, doc_type, **kwargs)

    def bulk(self, body, index=None, doc_type=None, **kwargs):
        return self.client.bulk(body, index, doc_type, **kwargs)

    def msearch(self, body, index=None, doc_type=None, **kwargs):
        return self.client.msearch(body, index, doc_type, **kwargs)

    def mpercolate(self, body, index=None, doc_type=None, **kwargs):
        return self.client.mpercolate(body, index, doc_type, **kwargs)

    # Scroll methods
    # ==============
    # The underlying client does not require an index to perform scroll.

    def scroll(self, scroll_id, **kwargs):
        return self.client.scroll(scroll_id, **kwargs)

    def clear_scroll(self, scroll_id, body=None, **kwargs):
        return self.client.clear_scroll(scroll_id, body, **kwargs)

    # Query methods
    # =============
    # The underlying client requires index names (or alias names) to perform
    # queries. The connection wrapper overrides these client methods to
    # automatically uses the configured names (indices and/or aliases).

    def create(self, doc_type, body, doc_id=None, **kwargs):
        return self.client.create(
            self.indices, doc_type, body, doc_id, **kwargs)

    def index(self, doc_type, body, doc_id=None, **kwargs):
        return self.client.index(
            self.indices, doc_type, body, doc_id, **kwargs)

    def exists(self, doc_id, doc_type='_all', **kwargs):
        return self.client.exists(self.indices, doc_id, doc_type, **kwargs)

    def get(self, doc_id, doc_type='_all', **kwargs):
        return self.client.get(self.indices, doc_id, doc_type, **kwargs)

    def get_source(self, doc_id, doc_type='_all', **kwargs):
        return self.client.get_source(self.indices, doc_id, doc_type, **kwargs)

    def update(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.update(
            self.indices, doc_type, doc_id, body, **kwargs)

    def search(self, doc_type=None, body=None, **kwargs):
        return self.client.search(self.indices, doc_type, body, **kwargs)

    def search_shards(self, doc_type=None, **kwargs):
        return self.client.search_shards(self.indices, doc_type, **kwargs)

    def search_template(self, doc_type=None, body=None, **kwargs):
        return self.client.search_template(
            self.indices, doc_type, body, **kwargs)

    def explain(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.explain(
            self.indices, doc_type, doc_id, body, **kwargs)

    def delete(self, doc_type, doc_id, **kwargs):
        return self.client.delete(self.indices, doc_type, doc_id, **kwargs)

    def count(self, doc_type=None, body=None, **kwargs):
        return self.client.count(self.indices, doc_type, body, **kwargs)

    def delete_by_query(self, doc_type=None, body=None, **kwargs):
        return self.client.delete_by_query(
            self.indices, doc_type, body, **kwargs)

    def suggest(self, body, **kwargs):
        return self.client.suggest(body, self.indices, **kwargs)

    def percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self.client.percolate(
            self.indices, doc_type, doc_id, body, **kwargs)

    def count_percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self.client.count_percolate(
            self.indices, doc_type, doc_id, body, **kwargs)

    def mlt(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.mlt(self.indices, doc_type, doc_id, body, **kwargs)

    def termvector(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.termvector(
            self.indices, doc_type, doc_id, body, **kwargs)

    def mtermvectors(self, doc_type=None, body=None, **kwargs):
        return self.client.mtermvectors(self.indices, doc_type, body, **kwargs)

    def benchmark(self, doc_type=None, body=None, **kwargs):
        return self.client.benchmark(self.indices, doc_type, body, **kwargs)

    def abort_benchmark(self, name=None, **kwargs):
        return self.client.abort_benchmark(name, **kwargs)

    def list_benchmarks(self, doc_type=None, **kwargs):
        return self.client.list_benchmarks(self.indices, doc_type, **kwargs)


# ElasticSearch backends
# ======================

class SimpleHttpBackend(BaseElasticsearchBackend):
    """Connection backend using the ``urllib3`` connection class."""
    connection_class = Urllib3HttpConnection


class SimpleRequestsHttpBackend(BaseElasticsearchBackend):
    """Connection backend using the HTTP for Human request connection class."""
    connection_class = RequestsHttpConnection


class SimpleThriftBackend(BaseElasticsearchBackend):
    """Connection backend using the Thrift experimental connection class."""
    connection_class = ThriftConnection


class SimpleMemcachedBackend(BaseElasticsearchBackend):
    """Connection backend using the Memcache connection class.

    As describe in the ``MemcachedConnection``, a plugin must be installed in
    the ElasticSearch cluster in order to work.
    """
    connection_class = MemcachedConnection
