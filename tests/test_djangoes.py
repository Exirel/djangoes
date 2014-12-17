from unittest.case import TestCase

from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings

from djangoes import (ConnectionHandler,
                      IndexDoesNotExist,
                      ConnectionDoesNotExist,
                      load_backend)
from djangoes.backends import Base, elasticsearch


class TestConnectionHandler(TestCase):
    """Test the ConnectionHandler class.

    The ConnectionHandler is a major entry point for a good integration of
    ElasticSearch in a Django project. It must ensure appropriate default
    values, settings conformity, and prepare tests settings.
    """

    # Test behavior with the default and/or empty values
    # ==================================================
    # Makes assertions about the default behavior when nothing is configured,
    # or when very few information is given. Using djangoes should be as
    # transparent as possible, in particular with the default behavior.

    def test_empty(self):
        """Assert an empty configuration fallback on default values."""
        servers = {}
        indices = {}

        handler = ConnectionHandler(servers, indices)

        # A default alias appear in servers, while nothing changed in indices.
        assert handler.servers == {'default': {}}
        assert handler.indices == indices

    def test_empty_with_default(self):
        """Assert the ensured default configuration is acceptable as input."""
        servers = {
            'default': {
                'ENGINE': 'djangoes.backends.elasticsearch',
                'HOSTS': [],
                'PARAMS': {},
                'INDICES': []
            }
        }
        indices = {
            'index': {
                'NAME': 'index',
                'ALIASES': []
            }
        }

        handler = ConnectionHandler(servers, indices)

        # Both must be equal, without changes.
        assert handler.servers == servers
        assert handler.indices == indices

    def test_empty_with_default_fallback(self):
        """Assert the fallback configuration is acceptable as input."""
        servers = {
            'default': {}
        }
        indices = {}

        handler = ConnectionHandler(servers, indices)

        assert handler.servers == {'default': {}}
        assert handler.indices == {}

    # Test with django project settings
    # =================================

    def test_project_settings_by_default(self):
        """Assert values come from the django project settings if not given."""
        servers = {
            'default': {},
            'by_settings': {}
        }
        indices = {
            'index_by_settings': {}
        }
        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            # No argument
            handler = ConnectionHandler()
            # Servers and indices are the one set in django settings.
            assert handler.servers == servers
            assert handler.indices == indices

    # Test improperly configured behaviors
    # ====================================

    def test_improperly_configured_servers(self):
        """Assert raise when settings are not empty but without `default`."""
        servers = {
            'not_default': {}
        }

        handler = ConnectionHandler(servers, {})

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.servers

        assert str(raised.exception) == 'You must define a \'default\' ElasticSearch server'

    # Test ensure default values
    # ==========================

    # Server

    def test_empty_ensure_server_defaults(self):
        """Assert default values are set properly on an empty server."""
        handler = ConnectionHandler({}, {})
        handler.ensure_server_defaults('default')

        default_server = handler.servers['default']

        expected_server = {
            'ENGINE': 'djangoes.backends.elasticsearch',
            'HOSTS': [],
            'PARAMS': {},
            'INDICES': []
        }

        assert default_server == expected_server

    def test_ensure_server_defaults_not_exists(self):
        """Assert raise when the argument given is not a configured server."""
        servers = {}
        indices = {}

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(ConnectionDoesNotExist) as raised:
            handler.ensure_server_defaults('index')

        assert str(raised.exception) == '%r' % 'index'

    # Index

    def test_empty_ensure_index_defaults(self):
        """Assert default values are set properly on an empty index."""
        indices = {
            'index': {}
        }

        handler = ConnectionHandler({}, indices)
        handler.ensure_index_defaults('index')

        index = handler.indices['index']

        expected_index = {
            'NAME': 'index',
            'ALIASES': []
        }

        assert index == expected_index

    def test_ensure_index_defaults_not_exists(self):
        """Assert raise when the argument given is not a configured index."""
        servers = {}
        indices = {}

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.ensure_index_defaults('index')

        assert str(raised.exception) == '%r' % 'index'

    # Test prepare test settings
    # ==========================

    # Prepare server

    def test_empty_prepare_server_test_settings(self):
        """Assert prepare adds a TEST key in the defaul server's settings."""
        servers = {
            'default': {
                'ENGINE': 'djangoes.backends.elasticsearch'
            }
        }

        handler = ConnectionHandler(servers, {})
        handler.prepare_server_test_settings('default')

        default_server = handler.servers['default']

        expected_test_server = {}

        assert 'TEST' in default_server
        assert default_server['TEST'] == expected_test_server

    def test_prepare_server_test_settings_not_exists(self):
        """Assert raise when the argument given is not a configured server."""
        servers = {
            'default': {
                'ENGINE': 'djangoes.backends.elasticsearch'
            }
        }
        indices = {}

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(ConnectionDoesNotExist) as raised:
            handler.prepare_server_test_settings('index')

        assert str(raised.exception) == '%r' % 'index'

    # Prepare index

    def test_empty_prepare_index_test_settings(self):
        indices = {
            'index': {}
        }

        handler = ConnectionHandler({}, indices)
        handler.ensure_index_defaults('index')
        handler.prepare_index_test_settings('index')

        index = handler.indices['index']

        expected_test_index = {
            'NAME': 'index_test',
            'ALIASES': []
        }

        assert 'TEST' in index
        assert index['TEST'] == expected_test_index

    def test_prepare_index_test_settings_not_exists(self):
        """Assert raise when the argument given is not a configured index."""
        servers = {}
        indices = {}

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.prepare_index_test_settings('index')

        assert str(raised.exception) == '%r' % 'index'

    def test_prepare_index_test_settings_use_alias_not_index_name(self):
        """Assert raise even if the index NAME is given as argument.

        The prepare_index_test_settings method expects an index alias as used
        in the indices dict, not its NAME (nor any of its ALIASES).
        """
        servers = {}
        indices = {
            'index': {
                'NAME': 'not_this_index',
                'ALIASES': ['not_this_index']
            }
        }

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.prepare_index_test_settings('not_this_index')

        assert str(raised.exception) == '%r' % 'not_this_index'

    def test_prepare_index_test_settings_name_improperly_configured(self):
        """Assert raise when name and test name are the same."""
        servers = {}
        indices = {
            'index': {
                'NAME': 'index_production_name',
                'ALIASES': [],
                'TEST': {
                    'NAME': 'index_production_name',
                    'ALIASES': [],
                }
            }
        }

        handler = ConnectionHandler(servers, indices)

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.prepare_index_test_settings('index')

        assert str(raised.exception) == (
            'Index \'index\' uses improperly the same NAME and TEST\'s NAME '
                'settings: \'index_production_name\'.'
        )

    def test_prepare_index_test_settings_aliases_improperly_configured(self):
        """Assert raise when name and test name are the same."""
        servers = {}
        indices = {
            'index': {
                'NAME': 'index',
                'ALIASES': ['alias_prod', 'alias_prod_2'],
                'TEST': {
                    'NAME': 'index_valid_test_name',
                    'ALIASES': ['alias_prod', 'alias_test']
                }
            }
        }

        handler = ConnectionHandler(servers, indices)
        handler.ensure_index_defaults('index')

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.prepare_index_test_settings('index')

        assert str(raised.exception) == (
            'Index \'index\' uses improperly the same index alias in ALIASES '
            'and in TEST\'s ALIASES settings: \'alias_prod\'.'
        )

    # Test get server indices
    # =======================

    def test_empty_get_server_indices(self):
        """Assert there is no index by default, ie. `_all` will be used.

        ElasticSearch allows query on all indices. It is not safe for testing
        purposes, but it does not have to be checked in the connection handler.
        """
        handler = ConnectionHandler({}, {})

        # Yes, it is acceptable to get indices from a non-configured servers.
        # The purpose of get_server_indices is not to validate the input.
        test_server = {
            'INDICES': []
        }

        indices = handler.get_server_indices(test_server)

        assert indices == {}

    def test_get_server_indices(self):
        """Assert indices are found for a given server."""
        servers = {}
        indices = {
            'used': {},
            'not_used': {}
        }
        handler = ConnectionHandler(servers, indices)

        test_server = {
            'INDICES': ['used'],
        }

        indices = handler.get_server_indices(test_server)
        expected_indices = {
            'used': {
                'NAME': 'used',
                'ALIASES': [],
                'TEST': {
                    'NAME': 'used_test',
                    'ALIASES': []
                }
            }
        }

        assert indices == expected_indices

    # Test backend loading
    # ====================
    # Backend loading takes the given settings to import a module and
    # instantiate a subclass of djangoes.backends.Base.

    def test_function_load_backend(self):
        """Assert load_backend function imports and returns the given module.

        An external function is used to import the module and does one simple
        task: import a module and catch ImportError to raise a djangoes custom
        error.

        """
        mod = load_backend('os')
        assert hasattr(mod, 'path')

        sub_mod = load_backend('os.path')
        assert hasattr(sub_mod, 'isfile')

        with self.assertRaises(ImproperlyConfigured) as raised:
            load_backend('module.does.not.exist')

        assert str(raised.exception) == '\n'.join(
            ['\'module.does.not.exist\' isn\'t an available ElasticSearch backend.',
             'Error was: No module named \'module\''])

    def test_load_backend(self):
        """Assert load_backend method loads the configured server engine."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend'
            }
        }
        indices = {}
        handler = ConnectionHandler(servers, indices)

        result = handler.load_backend('default')

        assert isinstance(result, Base)
        assert result.alias == 'default'
        assert result.indices == []
        assert result.index_names == []

    def test_load_backend_with_index(self):
        servers = {
            'default': {
                'ENGINE': 'tests.backend',
                'INDICES': ['index_1'],
            }
        }
        indices = {
            'index_1': {
                'NAME': 'index_1',
                'ALIASES': ['alias_1', 'alias_2'],
            }
        }
        handler = ConnectionHandler(servers, indices)

        result = handler.load_backend('default')

        assert sorted(result.indices) == ['alias_1', 'alias_2']
        assert result.index_names == ['index_1']

    def test_load_backend_with_indices(self):
        servers = {
            'default': {
                'ENGINE': 'tests.backend',
                'INDICES': ['index_1', 'index_2'],
            }
        }
        indices = {
            'index_1': {
                'NAME': 'index_1',
                'ALIASES': ['alias_1', 'alias_2'],
            },
            'index_2': {
                'NAME': 'index_2_name',
            }
        }
        handler = ConnectionHandler(servers, indices)

        result = handler.load_backend('default')

        assert sorted(result.indices) == ['alias_1', 'alias_2', 'index_2_name']
        assert sorted(result.index_names) == ['index_1', 'index_2_name']

    # Test loading of backends.elasticsearch
    # ======================================

    def test_loading_elasticsearch(self):
        servers = {
            'default': {
                'ENGINE': 'djangoes.backends.elasticsearch'
            }
        }
        indices = {}

        handler = ConnectionHandler(servers, indices)

        result = handler.load_backend('default')

        assert isinstance(result, elasticsearch.ConnectionWrapper)

    # Test object and attributes manipulation
    # =======================================

    def test_iterable(self):
        """Assertions about list behavior of ConnectionHandler."""
        servers = {
            'default': {},
            'task': {},
        }
        indices = {}

        handler = ConnectionHandler(servers, indices)

        assert sorted(list(handler)) == ['default', 'task']

    def test_items(self):
        """Assertions about key:value behavior of ConnectionHandler."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend',
                'INDICES': ['index_1'],
            },
        }
        indices = {
            'index_1': {},
            'index_2': {}
        }

        handler = ConnectionHandler(servers, indices)

        # Get the connection wrapper
        wrapper = handler['default']
        assert wrapper.indices == ['index_1']

        # Change handler settings
        handler.servers['default']['INDICES'] = ['index_2']

        # The wrapper is not updated
        wrapper = handler['default']
        assert wrapper.indices == ['index_1']

        # Delete the `default` connection 
        del handler['default']

        # The new wrapper now use the new index
        wrapper = handler['default']
        assert wrapper.indices == ['index_2']

        # Also, set item works without control
        handler['something'] = 'else'
        assert handler['something'] == 'else'

    def test_all(self):
        """Assert all connection wrappers are returned."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend',
            },
            'task': {
                'ENGINE': 'tests.backend'
            }
        }
        indices = {}
        handler = ConnectionHandler(servers, indices)

        all_connections = handler.all()

        assert len(all_connections) == 2
        assert isinstance(all_connections[0], Base)
        assert isinstance(all_connections[1], Base)

        assert sorted([c.alias for c in all_connections]) == ['default', 'task']


class TestProxyConnectionHandler(TestCase):
    def test_attributes(self):
        # Local import to manipulate elements
        from djangoes import connections, connection

        connections._servers = {
            'default': {
                'ENGINE': 'tests.backend'
            }
        }
        connections._indices = {}

        # Existing attribute.
        assert connection.alias == 'default'

        # New attribute.
        assert not hasattr(connection, 'new_attribute')

        connections['default'].new_attribute = 'test_value'

        assert hasattr(connection, 'new_attribute')
        assert connection.new_attribute == 'test_value'

        del connection.new_attribute

        assert not hasattr(connection, 'new_attribute')
        assert not hasattr(connections['default'], 'new_attribute')

        connection.new_attribute = 'test_new_attribute_again'

        assert hasattr(connection, 'new_attribute')
        assert hasattr(connections['default'], 'new_attribute')

        assert connection == connections['default']
        assert not (connection != connections['default'])
