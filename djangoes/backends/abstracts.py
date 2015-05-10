"""Module djangoes.backends.abstracts provides abstract classes for backends.

All backends are expecting to subclass these abstract classes and to implement
their behaviors.
"""
from django.utils.functional import cached_property


ATTR_ERROR_TEMPLATE = ('\'%s\' object has no attribute \'%s\', '
                       'is it implemented?')


class Base(object):
    """ElasticSearch backend wrapper base."""
    def __init__(self, alias, server, indices):
        """Instantiate a connection wrapper."""
        self.alias = alias
        self.server = server
        self.server_indices = indices
        self.client = None

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
        given by ``indices``, for example when one wants to create them.
        """
        return list(
            set(
                index['NAME'] for index in self.server_indices.values()
            )
        )

    def get_alias_names(self):
        """Build and return the list of alias names.

        This create a list of unique alias names, without using their indices.
        It can be useful to get alias names instead of their usage names, as
        given by ``indices`` as it would gives index names when no alias is
        configured - which is not always what is needed.
        """
        return list(
            set(
                alias
                for index in self.server_indices.values()
                for alias in index['ALIASES']
            )
        )

    def get_indices_with_settings(self):
        """Build and return a dict of indices with their settings.

        This create a dict where each key is a index name, and each value is
        the index key's settings (as used to created the index). It is useful
        when one wants to create an index with its settings for the given
        connection.
        """
        return {
            index['NAME']: index['SETTINGS']
            for index in self.server_indices.values()
        }

    @cached_property
    def indices(self):
        """Cached property upon :meth:`get_indices`."""
        return self.get_indices()

    @cached_property
    def index_names(self):
        """Cached property upon :meth:`get_index_names`."""
        return self.get_index_names()

    @cached_property
    def alias_names(self):
        """Cached property upon :meth:`get_alias_names`."""
        return self.get_alias_names()
