from elasticsearch.client import Elasticsearch, Transport

from . import Base


class ConnectionWrapper(Base):
    """Connection wrapper based on the ElasticSearch official library."""
    transport_class = Transport

    def __init__(self, alias, server, indices):
        Base.__init__(self, alias, server, indices)

    def configure_client(self):
        hosts = self.server['HOSTS']
        params = self.server['PARAMS']

        self._es = Elasticsearch(
            hosts, transport_class=self.transport_class, **params)

    def __getattribute__(self, attr):
        """Proxy for attributes and methods to the underlying ES client."""
        return getattr(self._es, attr)

    # Query methods 
    # =============
    # The underlying client requires index names (or alias names) to perform
    # queries. The connection wrapper overrides these client methods to
    # automatically uses the configured names (indices and/or aliases).

    def create(self, doc_type, body, doc_id=None, **kwargs):
        return self._es.create(self.indices, doc_type, body, doc_id, **kwargs)

    def index(self, doc_type, body, doc_id=None, **kwargs):
        return self._es.index(self.indices, doc_type, body, doc_id, **kwargs)

    def exists(self, doc_id, doc_type='_all', **kwargs):
        return self._es.exists(self.indices, doc_id, doc_type, **kwargs)

    def get(self, doc_id, doc_type='_all', **kwargs):
        return self._es.get(self.indices, doc_id, doc_type, **kwargs)

    def get_source(self, doc_id, doc_type='_all', **kwargs):
        return self._es.get_source(self.indices, doc_id, doc_type, **kwargs)

    def update(self, doc_type, doc_id, body=None, **kwargs):
        return self._es.update(self.indices, doc_type, doc_id, body, **kwargs)

    def search(self, doc_type=None, body=None, **kwargs):
        return self._es.search(self.indices, doc_type, body, **kwargs)

    def search_shards(self, doc_type=None, **kwargs):
        return self._es.search_shards(self.indices, doc_type, **kwargs)

    def search_template(self, doc_type=None, body=None, **kwargs):
        return self._es.search_template(self.indices, doc_type, body, **kwargs)

    def explain(self, doc_type, doc_id, body=None, **kwargs):
        return self._es.explain(self.indice, doc_type, doc_id, body, **kwargs)

    def delete(self, doc_type, doc_id, **kwargs):
        return self._es.delete(self.indices, doc_type, doc_id, **kwargs)

    def count(self, index=None, doc_type=None, body=None, **kwargs):
        return self._es.count(self.indices, doc_type, body, **kwargs)

    def delete_by_query(self, index, doc_type=None, body=None, **kwargs):
        return self._es.delete_by_query(self.indices, doc_type, body, **kwargs)

    def percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self._es.percolate(self.indices, doc_type, doc_id, body, **kwargs)

    def count_percolate(self, doc_type, doc_id=None, body=None, **kwargs):
        return self._es.count_percolate(self.indices, doc_type, doc_id, body, **kwargs)

    def mlt(self, doc_type, doc_id, body=None, **kwargs):
        return self._es.mlt(self.indices, doc_type, doc_id, body, **kwargs)

    def termvector(self, doc_type, doc_id, body=None, **kwargs):
        return self._es.termvector(self.indices, doc_type, doc_id, body, **kwargs)

    def mtermvectors(self, index=None, doc_type=None, body=None, **kwargs):
        return self._es.mtermvectors(self.indices, doc_type, body, **kwargs)

    def benchmark(self, index=None, doc_type=None, body=None, **kwargs):
        return self._es.benchmark(self.indices, doc_type, body, **kwargs)

    def list_benchmarks(self, doc_type=None, **kwargs):
        return self._es.list_benchmarks(self.indices, doc_type, **kwargs)
