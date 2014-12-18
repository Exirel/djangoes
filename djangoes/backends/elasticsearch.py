from elasticsearch.client import Elasticsearch, Transport

from . import Base, MetaClientBase


class MetaClient(MetaClientBase):
    """Meta client class for the `elasticsearch` backend.

    Act as a proxy to the internal ElasticSearch client's attributes.
    """
    @property
    def indices(self):
        """Access to meta API about indices.

        Return the client's indices attribute.
        """
        return self.conn.client.indices

    @property
    def cluster(self):
        """Access to meta API about cluster.

        Return the client's cluster attribute.
        """
        return self.conn.client.cluster

    @property
    def nodes(self):
        """Access to meta API about nodes.

        Return the client's nodes attribute.
        """
        return self.conn.client.nodes

    @property
    def snapshot(self):
        """Access to meta API about snapshot.

        Return the client's snapshot attribute.
        """
        return self.conn.client.snapshot


class ConnectionWrapper(Base):
    """Connection wrapper based on the ElasticSearch official library."""
    transport_class = Transport
    meta_client_class = MetaClient

    def __init__(self, alias, server, indices):
        super(ConnectionWrapper, self).__init__(alias, server, indices)
        self.client = None

    def configure_client(self):
        """Instantiate and configure the ElasticSearch client.

        It simply takes the given HOSTS list and uses PARAMS as the keyword
        arguments of the Elasticsearch class.

        The client's transport_class is given by the class attribute
        `transport_class`.
        """
        hosts = self.server['HOSTS']
        params = self.server['PARAMS']

        #pylint: disable=star-args
        self.client = Elasticsearch(
            hosts, transport_class=self.transport_class, **params)

    # Server methods
    # ==============
    # The underlying client does not require index names to perform server
    # related queries, such as "ping" or "info". The connection wrapper act
    # for them as a proxy.

    def ping(self, params=None):
        return self.client.ping(params)

    def info(self, params=None):
        return self.client.info(params)

    def put_script(self, lang, script_id, body, params=None):
        return self.client.put_script(lang, script_id, body, params)

    def get_script(self, lang, script_id, params=None):
        return self.client.get_script(lang, script_id, params)

    def delete_script(self, lang, script_id, params=None):
        return self.client.delete_script(lang, script_id, params)

    def put_template(self, template_id, body, params=None):
        return self.client.put_template(template_id, body, params)

    def get_template(self, template_id, body=None, params=None):
        return self.client.get_template(template_id, body, params)

    def delete_template(self, template_id=None, params=None):
        return self.client.delete_template(template_id, params)

    # Bulk methods
    # ============
    # The underlying client does not require index names, but it can be used.
    # As it makes sense to not give an index, developers are free to use these
    # as they want, as long as they are careful.

    def mget(self, body, index=None, doc_type=None, params=None):
        return self.client.mget(body, index, doc_type, params)

    def bulk(self, body, index=None, doc_type=None, params=None):
        return self.client.bulk(body, index, doc_type, params)

    def msearch(self, body, index=None, doc_type=None, params=None):
        return self.client.msearch(body, index, doc_type, params)

    def mpercolate(self, body, index=None, doc_type=None, params=None):
        return self.client.mpercolate(body, index, doc_type, params)

    # Scroll methods
    # ==============
    # The underlying client does not require an index to perform scroll.

    def scroll(self, scroll_id, params=None):
        return self.client.scroll(scroll_id, params)

    def clear_scroll(self, scroll_id, body=None, params=None):
        return self.client.clear_scroll(scroll_id, body, params)

    # Query methods
    # =============
    # The underlying client requires index names (or alias names) to perform
    # queries. The connection wrapper overrides these client methods to
    # automatically uses the configured names (indices and/or aliases).

    def create(self, doc_type, body, doc_id=None, **kwargs):
        return self.client.create(self.indices, doc_type, body, doc_id, **kwargs)

    def index(self, doc_type, body, doc_id=None, **kwargs):
        return self.client.index(self.indices, doc_type, body, doc_id, **kwargs)

    def exists(self, doc_id, doc_type='_all', **kwargs):
        return self.client.exists(self.indices, doc_id, doc_type, **kwargs)

    def get(self, doc_id, doc_type='_all', **kwargs):
        return self.client.get(self.indices, doc_id, doc_type, **kwargs)

    def get_source(self, doc_id, doc_type='_all', **kwargs):
        return self.client.get_source(self.indices, doc_id, doc_type, **kwargs)

    def update(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.update(self.indices, doc_type, doc_id, body, **kwargs)

    def search(self, doc_type=None, body=None, **kwargs):
        return self.client.search(self.indices, doc_type, body, **kwargs)

    def search_shards(self, doc_type=None, **kwargs):
        return self.client.search_shards(self.indices, doc_type, **kwargs)

    def search_template(self, doc_type=None, body=None, **kwargs):
        return self.client.search_template(self.indices, doc_type, body, **kwargs)

    def explain(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.explain(self.indices, doc_type, doc_id, body, **kwargs)

    def delete(self, doc_type, doc_id, **kwargs):
        return self.client.delete(self.indices, doc_type, doc_id, **kwargs)

    def count(self, doc_type=None, body=None, **kwargs):
        return self.client.count(self.indices, doc_type, body, **kwargs)

    def delete_by_query(self, doc_type=None, body=None, **kwargs):
        return self.client.delete_by_query(self.indices, doc_type, body, **kwargs)

    def suggest(self, body, params=None):
        return self.client.suggest(body, self.indices, params)

    def percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self.client.percolate(self.indices, doc_type, doc_id, body, **kwargs)

    def count_percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self.client.count_percolate(self.indices, doc_type, doc_id, body, **kwargs)

    def mlt(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.mlt(self.indices, doc_type, doc_id, body, **kwargs)

    def termvector(self, doc_type, doc_id, body=None, **kwargs):
        return self.client.termvector(self.indices, doc_type, doc_id, body, **kwargs)

    def mtermvectors(self, doc_type=None, body=None, **kwargs):
        return self.client.mtermvectors(self.indices, doc_type, body, **kwargs)

    def benchmark(self, doc_type=None, body=None, **kwargs):
        return self.client.benchmark(self.indices, doc_type, body, **kwargs)

    def abort_benchmark(self, name=None, params=None):
        return self.client.abort_benchmark(name, params)

    def list_benchmarks(self, doc_type=None, **kwargs):
        return self.client.list_benchmarks(self.indices, doc_type, **kwargs)
