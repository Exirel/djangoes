from importlib import import_module
from threading import local

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property


#  Name of the default ElasticSearch server connection
DEFAULT_ES_ALIAS = 'default'


def load_backend(backend_name):
    try:
        return import_module(backend_name)
    except ImportError as e_user:
        error_msg = ("%r isn't an available ElasticSearch backend.\n"
                     "Error was: %s" % 
                     (backend_name, e_user))
        raise ImproperlyConfigured(error_msg)


class ConnectionDoesNotExist(KeyError):
    msg_tpl = 'The connection \'%s\' doesn\'t exist'
    def __init__(self, alias, *args, **kwargs):
        KeyError.__init__(self, self.msg_tpl % alias, *args, **kwargs)
        self.alias = alias


class IndexDoesNotExist(KeyError):
    msg_tpl = 'The index \'%s\' doesn\'t exist'
    def __init__(self, alias, *args, **kwargs):
        KeyError.__init__(self, self.msg_tpl % alias, *args, **kwargs)
        self.alias = alias


class ConnectionHandler(object):
    """Handle connections to ElasticSearch.

    Based on django.db.utils.ConnectionHandler, it aims to be an interface to
    integrate ElasticSearch connections in the same way database connections
    are integrated in Django.

    However, instead of relaying on one setting variable, it needs two:

    * `servers`: ElasticSearch clusters connections settings (host, port, etc.)
    * `indices`: indices (or indexes) settings (name, aliases, analyzers, etc.)

    These two will be defined in the django project settings with `ES_SERVERS`
    and `ES_INDICES`.
    """
    def __init__(self, servers=None, indices=None):
        """Instantiate a ConnectionHandler.

        Both `servers` and `indices` are optional arguments, and they have the
        same structure as `settings.ES_SERVERS` and `settings.ES_INDICES`.
        """
        self._servers = servers
        self._indices = indices
        self._connections = local()

    @cached_property
    def servers(self):
        if self._servers is None:
            # ES_SERVERS is not required.
            self._servers = getattr(settings, 'ES_SERVERS', {})

        if self._servers == {}:
            self._servers = {
                # Nothing is required for a default connection.
                # Yeah, it works out of the box. Just magic.
                DEFAULT_ES_ALIAS: {}
            }

        if DEFAULT_ES_ALIAS not in self._servers:
            raise ImproperlyConfigured(
                'You must define a \'%s\' ElasticSearch server'
                % DEFAULT_ES_ALIAS)

        return self._servers

    @cached_property
    def indices(self):
        if self._indices is None:
            # ES_INDICES is not required.
            self._indices = getattr(settings, 'ES_INDICES', {})

        return self._indices

    def ensure_server_defaults(self, alias):
        """Puts the defaults into the settings dictionary for `alias`."""
        try:
            server = self.servers[alias]
        except KeyError:
            raise ConnectionDoesNotExist(alias)

        server.setdefault('ENGINE', 'djangoes.backends.elasticsearch')
        server.setdefault('HOSTS', [])
        server.setdefault('PARAMS', {})
        server.setdefault('INDICES', [])

    def ensure_index_defaults(self, alias):
        """Puts the defaults into the settings dictionary for `alias`."""
        try:
            index = self.indices[alias]
        except KeyError:
            raise IndexDoesNotExist(alias)

        index.setdefault('NAME', alias)
        index.setdefault('ALIASES', [])

    def prepare_server_test_settings(self, alias):
        """Makes sure the test settings are available in `TEST`."""
        try:
            server = self.servers[alias]
        except KeyError:
            raise ConnectionDoesNotExist(alias)

        # TODO: Add more than a simple `TEST` key.
        # This will need to dig into ElasticSearch optimization stuff.
        # Yay!
        server.setdefault('TEST', {})

    def prepare_index_test_settings(self, alias):
        """Makes sure the test settings are available in `TEST`."""
        # TODO: Prepare these settings, for real.
        try:
            index = self.indices[alias]
        except KeyError:
            raise IndexDoesNotExist(alias)

        test_settings = index.setdefault('TEST', {})

        # Handle the TEST's NAME
        name = index['NAME']
        test_name = test_settings.setdefault('NAME', '%s_test' % name)

        if test_name == name:
            raise ImproperlyConfigured(
                'Index \'%s\' uses improperly the same NAME and TEST\'s NAME '
                'settings: \'%s\'.' % (alias, name))

        # Handle the TEST's ALIASES
        aliases = index['ALIASES']
        test_aliases = test_settings.setdefault('ALIASES',
                                                ['%s_test' % alias_name
                                                 for alias_name in aliases])

        for test_alias_name in test_aliases:
            if test_alias_name in aliases:
                raise ImproperlyConfigured(
                    'Index \'%s\' uses improperly the same index alias in '
                    'ALIASES and in TEST\'s ALIASES settings: \'%s\'.'
                    % (alias, test_alias_name))

    def get_server_indices(self, server):
        """Prepares and returns a given server's indices settings."""
        indices = server['INDICES']

        for alias in indices:
            self.ensure_index_defaults(alias)
            self.prepare_index_test_settings(alias)

        return [self.indices[alias] for alias in indices]

    def load_backend(self, alias):
        """Prepares and loads a backend for the given alias."""
        # Prepares the settings
        self.ensure_server_defaults(alias)
        self.prepare_server_test_settings(alias)

        # Gets the settings for `alias`
        server = self.servers[alias]
        indices = self.get_server_indices(server)

        # Loads the backend
        backend = load_backend(server['ENGINE'])

        return backend.ConnectionWrapper(alias, server, indices)

    def __getitem__(self, alias):
        if hasattr(self._connections, alias):
            # Returns cached instance
            return getattr(self._connections, alias)

        # Loads and caches the backend
        conn = self.load_backend(alias)
        # TODO: Or maybe a lazy configure?
        conn.configure_client()

        setattr(self._connections, alias, conn)

        return conn

    def __setitem__(self, key, value):
        setattr(self._connections, key, value)

    def __delitem__(self, key):
        delattr(self._connections, key)

    def __iter__(self):
        return iter(self.servers)

    def all(self):
        return [self[alias] for alias in self]


connections = ConnectionHandler()
