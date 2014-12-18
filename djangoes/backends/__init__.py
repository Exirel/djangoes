from django.utils.functional import cached_property


ATTR_ERROR_TEMPLATE = ('\'%s\' object has no attribute \'%s\', '
                       'is it implemented?')


class MetaClientBase(object):
    """ElasticSearch meta client base.

    The meta client aims to provide an interface to the "meta" API of
    ElasticSearch, ie. manipulation of indices (creation, deletion, etc.),
    of cluster and nodes (settings), and of snapshot (backup/restore).

    The base class exposes a simple interface with 4 main attributes that must
    be implemented in the child class:

        * indices
        * cluster
        * nodes
        * snapshot

    """
    def __init__(self, conn):
        """Instantiate the meta client with a connection wrapper."""
        self.conn = conn

    @property
    def indices(self):
        """Access to meta API about indices."""
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'indices'))

    @property
    def cluster(self):
        """Access to meta API about cluster."""
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'cluster'))

    @property
    def nodes(self):
        """Access to meta API about nodes."""
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'nodes'))

    @property
    def snapshot(self):
        """Access to meta API about snapshot."""
        raise AttributeError(ATTR_ERROR_TEMPLATE % (type(self), 'snapshot'))


class Base(object):
    """ElasticSearch backend wrapper base."""
    meta_client_class = MetaClientBase

    def __init__(self, alias, server, indices):
        """Instantiate a connection wrapper."""
        self.alias = alias
        self.server = server
        self.server_indices = indices
        self.meta = self.meta_client_class(self)

    def configure_client(self):
        """Configure the ElasticSearch client."""
        raise NotImplementedError

    def get_indices(self):
        """Build the list of indices or aliases used to query ElasticSearch.

        This creates a list composed of index names or alias names. If an index
        defined aliases, these aliases will be used instead of its own name.
        """
        indices = set()

        for index in self.server_indices.values():
            name = index['NAME']
            aliases = index['ALIASES']

            if aliases:
                for alias in index['ALIASES']:
                    indices.add(alias)
            else:
                indices.add(name)

        return list(indices)

    def get_index_names(self):
        """Build and return the list of index names.

        This create a list of unique index names, without using their aliases.
        It can be useful to get index names instead of their usage names, as
        given by `indices`, for example when one wants to create such indices.
        """
        return list(
            set(
                index['NAME'] for index in self.server_indices.values()
            )
        )

    @cached_property
    def indices(self):
        """Cached property upon get_indices method."""
        return self.get_indices()

    @cached_property
    def index_names(self):
        """Cached property upon get_index_names method."""
        return self.get_index_names()
