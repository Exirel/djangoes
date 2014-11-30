from django.utils.functional import cached_property


class Base(object):
    """ElasticSearch backend wrapper base."""
    def __init__(self, alias, server, indices):
        self.alias = alias
        self._server = server
        self._indices = indices
        self.configure_client()

    def configure_client(self):
        """Configures the ElasticSearch client."""
        raise NotImplementedError

    @cached_property
    def indices(self):
        """Builds the list of indices or aliases used to query ElasticSearch.

        This creates a list composed of index names or alias names. If an index
        defined aliases, these aliases will be used instead of its own name.
        """
        indices = set()

        for index in self._indices:
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
        return list(set(index['NAME'] for index in self._indices))
