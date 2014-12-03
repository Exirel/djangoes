from unittest.case import TestCase

from djangoes import ConnectionHandler


class TestConnectionHandler(TestCase):
    """Tests the ConnectionHandler class.

    The ConnectionHandler is a major entry point for a good integration of
    ElasticSearch in a Django project. It must ensure appropriate default
    values, settings conformity, and prepare tests settings.
    """

    # Tests behavior with the default and/or empty values
    # ===================================================
    # Makes assertions about the default behavior when nothing is configured,
    # or when very few information is given. Using djangoes should be as
    # transparent as possible, in particular with the default behavior.

    def test_empty(self):
        """Asserts an empty configuration fallback on default."""
        servers = {}
        indices = {}

        handler = ConnectionHandler(servers, indices)

        assert handler.servers == {'default': {}}
        assert handler.indices == {}

    def test_empty_with_default(self):
        """Asserts the default configuration is acceptable, indeed."""
        servers = {
            'default': {}
        }
        indices = {}

        handler = ConnectionHandler(servers, indices)

        assert handler.servers == {'default': {}}
        assert handler.indices == {}

    def test_empty_ensure_server_defaults(self):
        """Asserts default values are set properly on an empty server."""
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

    def test_empty_ensure_indices_defaults(self):
        """Asserts default values are set properly on an empty index."""
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

    def test_empty_prepare_server_test_settings(self):
        handler = ConnectionHandler({}, {})
        handler.ensure_server_defaults('default')
        handler.prepare_server_test_settings('default')

        default_server = handler.servers['default']

        expected_test_server = {}

        assert 'TEST' in default_server
        assert default_server['TEST'] == expected_test_server

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

    def test_empty_get_server_indices(self):
        """Asserts there is no index by default, ie. `_all` will be used.

        ElasticSearch allows query on all indices. It is not safe for testing
        purposes, but it does not have to be checked in the connection handler.
        """
        handler = ConnectionHandler({}, {})
        test_server = {
            'NAME': 'default',
            'INDICES': []
        }

        indices = handler.get_server_indices(test_server)

        assert indices == []
