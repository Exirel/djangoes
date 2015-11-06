from django.utils.functional import cached_property
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


DEFAULT_INDEX_ALIAS = 'default'


class IndexHandler:
    def __init__(self, connections, indices=None):
        self.connections = connections
        self._indices = indices

    @cached_property
    def indices(self):
        """Dict of indices configuration.

        The `indices` attribute come from the initial `indices` parameter used
        to instantiate the connections handler.

        Each key is supposed to be the alias name to an indices configuration,
        giving a list of index names and other parameters, such as index
        aliases.

        If no configurations is provided, it will use the django project
        setting ``ES_INDICES`` as a fallback.
        """
        if self._indices is None:
            # ES_INDICES is not required.
            self._indices = getattr(settings, 'ES_INDICES', {})

        if self._indices == {}:
            self._indices = {
                # Nothing is required for a default connection.
                # Yeah, it works out of the box. Just magic.
                DEFAULT_INDEX_ALIAS: {}
            }

        if DEFAULT_INDEX_ALIAS not in self._indices:
            raise ImproperlyConfigured(
                'You must define a \'%s\' ElasticSearch index'
                % DEFAULT_INDEX_ALIAS)

        return self._indices
