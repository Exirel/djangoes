from django.utils.functional import cached_property


ATTR_ERROR_TEMPLATE = ('\'%s\' object has no attribute \'%s\', '
                       'is it implemented?')


class MetaClientBase(object):
    def __init__(self, conn):
        self.conn = conn

    @property
    def indices(self):
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'indices'))

    @property
    def cluster(self):
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'cluster'))

    @property
    def nodes(self):
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'nodes'))

    @property
    def snapshot(self):
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'snapshot'))


class Base(object):
    """ElasticSearch backend wrapper base."""
    meta_client_class = MetaClientBase

    def __init__(self, alias, server, indices):
        self.alias = alias
        self._server = server
        self._indices = indices
        self.meta = self.meta_client_class(self)

    def configure_client(self):
        """Configure the ElasticSearch client."""
        raise NotImplementedError

    @cached_property
    def indices(self):
        """Build the list of indices or aliases used to query ElasticSearch.

        This creates a list composed of index names or alias names. If an index
        defined aliases, these aliases will be used instead of its own name.
        """
        indices = set()

        for index in self._indices.values():
            name = index['NAME']
            aliases = index['ALIASES']

            if aliases:
                for alias in index['ALIASES']:
                    indices.add(alias)
            else:
                indices.add(name)

        return list(indices)

    @cached_property
    def index_names(self):
        return list(set(index['NAME'] for index in self._indices.values()))
