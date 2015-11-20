"""Djangoes package aims to provide a simple way to integrate ElasticSearch.

This package mimics the behavior of the Django database configuration layer,
using project settings and a global connections handler.

The simplest way to use ``djangoes`` is to import ``djangoes.connection`` and
to perform queries with it::

   >>> from djangoes import connections
   >>> conn = connections['conn_name']
   >>> result = conn.search(...)

The :meth:`ConnectionHandler.load_backend` is called whenever a connection is
requested in the application, which will then call multiple methods to ensure
default values and test values.

There is a shortcut to get the default connection::

   >>> from djangoes import connection, connections
   >>> connection == connections['default']
   True
   >>> result = connection.search(...)

It works exactly like getting the ``default`` connection from ``connections``.

.. note::

    This module is based on the ``django.db`` module, which is quite simple in
    its way to deal with connections. The ``djangoes`` package hope to stay as
    simple as possible for everyone, and to take benefit from the hard works
    that make Django a great framework.

"""
from importlib import import_module
import os
from threading import local

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import cached_property


__version__ = '0.3.1'


#: Name of the default ElasticSearch server connection
DEFAULT_ES_ALIAS = 'default'


def load_backend(backend_class_path):
    """Import the given `backend_class_path` class and return it.

    This is a convenient function that raises a specific error message when
    the import of the `backend_class_path` raises an ImportError or an
    AttributeError.
    """
    parts = backend_class_path.split('.')
    backend_module, backend_class = '.'.join(parts[:-1]), parts[-1]

    try:
        return getattr(import_module(backend_module), backend_class)
    except (AttributeError, ImportError) as e_user:
        error_msg = ("%r isn't an available ElasticSearch backend.\n"
                     "Error was: %s" %
                     (backend_class_path, e_user))
        raise ImproperlyConfigured(error_msg)


class ConnectionDoesNotExist(KeyError):
    """Specific type of KeyError when a connection does not exist."""
    pass


class IndexDoesNotExist(KeyError):
    """Specific type of KeyError when an index does not exist."""
    pass


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
        self._pid = os.getpid()

    # Properties
    # ----------

    @cached_property
    def servers(self):
        """Dict of servers configuration.

        The `servers` attribute come from the initial `servers` parameter used
        to instantiate the connections handler.

        Each key is supposed to be the alias name to a server configuration,
        giving an engine, a list of hosts, and other backend parameters.

        If no configurations is provided, it will use the django project
        setting `ES_SERVERS` as a fallback.

        If the default configuration does not exist, a ImproperlyConfigured is
        raised.
        """
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
        """Dict of indices configuration.

        The `indices` attribute come from the initial `indices` parameter used
        to instantiate the connections handler.

        Each key is supposed to be the alias name to an indices configuration,
        giving a list of index names and other parameters, such as index
        aliases.

        If no configurations is provided, it will use the django project
        setting `ES_INDICES` as a fallback.
        """
        if self._indices is None:
            # ES_INDICES is not required.
            self._indices = getattr(settings, 'ES_INDICES', {})

        return self._indices

    # Ensure default values
    # ---------------------

    def ensure_server_defaults(self, alias):
        """Put the defaults into the settings dictionary for `alias`."""
        try:
            server = self.servers[alias]
        except KeyError:
            raise ConnectionDoesNotExist(alias)

        server.setdefault(
            'ENGINE', 'djangoes.backends.elasticsearch.SimpleHttpBackend')
        server.setdefault('HOSTS', [])
        server.setdefault('PARAMS', {})
        server.setdefault('INDICES', [])

    def ensure_index_defaults(self, alias):
        """Put the defaults into the settings dictionary for `alias`."""
        try:
            index = self.indices[alias]
        except KeyError:
            raise IndexDoesNotExist(alias)

        index.setdefault('NAME', alias)
        index.setdefault('ALIASES', [])
        index.setdefault('SETTINGS', None)

    # Prepare test values
    # -------------------

    def prepare_server_test_settings(self, alias):
        """Make sure the test settings are available in `TEST`."""
        try:
            server = self.servers[alias]
        except KeyError:
            raise ConnectionDoesNotExist(alias)

        test_settings = server.setdefault('TEST', {})
        test_settings.setdefault('INDICES', [])

    def prepare_index_test_settings(self, alias):
        """Make sure the test settings are available in `TEST`."""
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

        # Index settings are kept for testing purpose as it is related to the
        # content and not the test configuration to access/request documents
        # in the index.
        test_settings.setdefault('SETTINGS', index['SETTINGS'])

    # Utility
    # -------

    def get_server_indices(self, server):
        """Prepare and return a given server's indices settings.

        Do not validate if the given server is available in ``self.servers``:
        it is expected to find an ``INDICES`` key into `server` and that's all.

        It is expected to find indices configured with the same name in
        ``self.indices``.
        """
        indices = server['INDICES']

        for alias in indices:
            self.ensure_index_defaults(alias)
            self.prepare_index_test_settings(alias)

        return {alias: self.indices[alias].copy() for alias in indices}

    def load_backend(self, alias):
        """Prepare and load a backend for the given alias."""
        # Prepares the settings
        self.ensure_server_defaults(alias)
        self.prepare_server_test_settings(alias)

        # Gets the settings for `alias`
        server = self.servers[alias]
        indices = self.get_server_indices(server)

        # Loads the backend
        backend_class = load_backend(server['ENGINE'])

        return backend_class(alias, server, indices)

    def check_for_multiprocess(self):
        """
        Reset connections if PID has changed.

        When using multi-processing (or fork), one may want to use a connection
        already used by the main process. Therefore, we need to make sure we
        are not sharing connections between multiple process.

        This could happen because a fork on Linux won't copy an object after a
        fork until it is modified. The read-only mode will "share" connections
        and that's not what we want.

        """
        current_pid = os.getpid()

        if current_pid != self._pid:
            # PID is different, we need to reset all the previous connections.
            self._pid = current_pid
            self._connections = local()

    # Magic methods
    # -------------

    def __getitem__(self, alias):
        self.check_for_multiprocess()

        if hasattr(self._connections, alias):
            # Returns cached instance
            return getattr(self._connections, alias)

        # Loads and caches the backend
        conn = self.load_backend(alias)
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
        """Return all configured connection object.

        It is a shortcut method to get all connections instead of manually
        doing a list-comprehension each time all connections are needed.
        """
        return [self[alias] for alias in self]


#: Global connections handler for ``djangoes``.
#: One can import ``djangoes.connections`` and ask for a connection that will
#: be thread safe and configured through the project settings.
connections = ConnectionHandler()  #pylint: disable=invalid-name


class ConnectionProxy(object):
    """Proxy for the default ``ConnectionWrapper``'s attributes.

    This class is based on ``django.db.DefaultConnectionProxy`` used for the
    default database.
    """
    def __init__(self, alias):
        self.__dict__['alias'] = alias or DEFAULT_ES_ALIAS

    def __getattr__(self, item):
        return getattr(connections[self.__dict__['alias']], item)

    def __setattr__(self, name, value):
        return setattr(connections[self.__dict__['alias']], name, value)

    def __delattr__(self, name):
        return delattr(connections[self.__dict__['alias']], name)

    def __eq__(self, other):
        return connections[self.__dict__['alias']] == other

    def __ne__(self, other):
        return connections[self.__dict__['alias']] != other


#: Default connection to ElasticSearch.
#: This is equivalent to call ``djangoes.connections['default']``.
connection = ConnectionProxy(DEFAULT_ES_ALIAS)  #pylint: disable=invalid-name
