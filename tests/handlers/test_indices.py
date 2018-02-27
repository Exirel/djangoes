import unittest

from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings

from djangoes.handlers import connections, indices
from djangoes.exceptions import IndexDoesNotExist


class TestIndexHandler(unittest.TestCase):

    # Test behavior with the default and/or empty values
    # ==================================================
    # Makes assertions about the default behavior when nothing is configured,
    # or when very few information is given. Using djangoes should be as
    # transparent as possible, in particular with the default behavior.

    def test_empty(self):
        """Assert an empty configuration fallback on default values."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {}

        handler = indices.IndexHandler(es_connections, conf)

        # A default alias appear in servers, while nothing changed in indices.
        assert handler.indices == {'default': {}}

    def test_empty_with_default(self):
        """Assert the ensured default configuration is acceptable as input."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'default': {
                'NAME': 'my_index',
                'SERVER': 'default',
                'SETTINGS': {}
            }
        }

        handler = indices.IndexHandler(es_connections, conf)

        # Must be equal, without changes.
        assert handler.indices == conf

    def test_empty_with_default_fallback(self):
        """Assert the fallback configuration is acceptable as input."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'default': {}
        }

        handler = indices.IndexHandler(es_connections, conf)

        assert handler.indices == {'default': {}}

    # Test with django project settings
    # =================================

    def test_project_settings_by_default(self):
        """Assert values come from the django project settings if not given."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'default': {},
            'index_by_settings': {}
        }
        with override_settings(ES_SERVERS={}, ES_INDICES=conf):
            # No argument
            handler = indices.IndexHandler(es_connections)
            # Indices are the one set in django settings.
            assert handler.indices == conf

    # Test improperly configured behaviors
    # ====================================

    def test_improperly_configured_servers(self):
        """Assert raise when settings are not empty but without `default`."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'not_default': {}
        }

        handler = indices.IndexHandler(es_connections, conf)

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.indices

        assert str(raised.exception) == "You must define a 'default' ElasticSearch index"

    # Test ensure default values
    # ==========================

    def test_empty_ensure_index_defaults(self):
        """Assert default values are set properly on an empty index."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'default': {}
        }

        handler = indices.IndexHandler(es_connections, conf)

        handler.ensure_index_defaults('default')

        index = handler.indices['default']

        expected_index = {
            'HANDLER': 'djangoes.handlers.indices.Index',
            'NAME': 'default',
            'ALIASES': [],
            'SETTINGS': None,
        }

        assert index == expected_index

    def test_ensure_index_defaults_not_exists(self):
        """Assert raise when the argument given is not a configured index."""
        es_connections = connections.ConnectionHandler({}, {})

        conf = {
            'default': {}
        }

        handler = indices.IndexHandler(es_connections, conf)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.ensure_index_defaults('does_not_exist')

        assert str(raised.exception) == '%r' % 'does_not_exist'

    # Test ensure default values
    # ==========================

    # Prepare index

    def test_empty_prepare_index_test_settings(self):
        conf = {
            'default': {}
        }

        conn = connections.ConnectionHandler({}, indices)
        handler = indices.IndexHandler(conn, conf)
        handler.ensure_index_defaults('default')
        handler.prepare_index_test_settings('default')

        index = handler.indices['default']

        expected_test_index = {
            'HANDLER': 'djangoes.handlers.indices.Index',
            'NAME': 'default_test',
            'ALIASES': [],
            'SETTINGS': None,
        }

        assert 'TEST' in index
        assert index['TEST'] == expected_test_index

    def test_prepare_index_test_settings_not_exists(self):
        """Assert raise when the argument given is not a configured index."""
        servers = {}
        conf = {}

        conn = connections.ConnectionHandler(servers, conf)
        handler = indices.IndexHandler(conn, conf)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.prepare_index_test_settings('index')

        assert str(raised.exception) == '%r' % 'index'

    def test_prepare_index_test_settings_use_alias_not_index_name(self):
        """Assert raise even if the index NAME is given as argument.

        The prepare_index_test_settings method expects an index alias as used
        in the indices dict, not its NAME (nor any of its ALIASES).
        """
        servers = {}
        conf = {
            'default': {
                'NAME': 'not_this_index',
                'ALIASES': ['not_this_index']
            }
        }

        conn = connections.ConnectionHandler(servers, conf)
        handler = indices.IndexHandler(conn, conf)

        with self.assertRaises(IndexDoesNotExist) as raised:
            handler.prepare_index_test_settings('not_this_index')

        assert str(raised.exception) == '%r' % 'not_this_index'

    def test_prepare_index_test_settings_name_improperly_configured(self):
        """Assert raise when name and test name are the same."""
        servers = {}
        conf = {
            'default': {
                'NAME': 'index_production_name',
                'ALIASES': [],
                'TEST': {
                    'NAME': 'index_production_name',
                    'ALIASES': [],
                }
            }
        }

        conn = connections.ConnectionHandler(servers, conf)
        handler = indices.IndexHandler(conn, conf)
        handler.ensure_index_defaults('default')

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.prepare_index_test_settings('default')

        assert str(raised.exception) == (
            'Index \'default\' uses improperly the same NAME and TEST\'s NAME '
                'settings: \'index_production_name\'.'
        )

    def test_prepare_index_test_settings_aliases_improperly_configured(self):
        """Assert raise when name and test name are the same."""
        servers = {}
        conf = {
            'default': {
                'NAME': 'index',
                'ALIASES': ['alias_prod', 'alias_prod_2'],
                'TEST': {
                    'NAME': 'index_valid_test_name',
                    'ALIASES': ['alias_prod', 'alias_test']
                }
            }
        }

        conn = connections.ConnectionHandler(servers, conf)
        handler = indices.IndexHandler(conn, conf)
        handler.ensure_index_defaults('default')

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.prepare_index_test_settings('default')

        assert str(raised.exception) == (
            'Index \'default\' uses improperly the same index alias in ALIASES '
            'and in TEST\'s ALIASES settings: \'alias_prod\'.'
        )
