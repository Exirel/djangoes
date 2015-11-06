import unittest

from django.core.exceptions import ImproperlyConfigured
from django.test.utils import override_settings

from djangoes.handlers import connections
from djangoes.handlers.indices import IndexHandler


class TestIndexHandler(unittest.TestCase):

    # Test behavior with the default and/or empty values
    # ==================================================
    # Makes assertions about the default behavior when nothing is configured,
    # or when very few information is given. Using djangoes should be as
    # transparent as possible, in particular with the default behavior.

    def test_empty(self):
        """Assert an empty configuration fallback on default values."""
        es_connections = connections.ConnectionHandler({}, {})

        indices = {}

        handler = IndexHandler(es_connections, indices)

        # A default alias appear in servers, while nothing changed in indices.
        assert handler.indices == {'default': {}}

    def test_empty_with_default(self):
        """Assert the ensured default configuration is acceptable as input."""
        es_connections = connections.ConnectionHandler({}, {})

        indices = {
            'default': {
                'NAME': 'my_index',
                'SERVER': 'default',
                'SETTINGS': {}
            }
        }

        handler = IndexHandler(es_connections, indices)

        # Must be equal, without changes.
        assert handler.indices == indices

    def test_empty_with_default_fallback(self):
        """Assert the fallback configuration is acceptable as input."""
        es_connections = connections.ConnectionHandler({}, {})

        indices = {
            'default': {}
        }

        handler = IndexHandler(es_connections, indices)

        assert handler.indices == {'default': {}}

    # Test with django project settings
    # =================================

    def test_project_settings_by_default(self):
        """Assert values come from the django project settings if not given."""
        es_connections = connections.ConnectionHandler({}, {})

        indices = {
            'default': {},
            'index_by_settings': {}
        }
        with override_settings(ES_SERVERS={}, ES_INDICES=indices):
            # No argument
            handler = IndexHandler(es_connections)
            # Indices are the one set in django settings.
            assert handler.indices == indices

    # Test improperly configured behaviors
    # ====================================

    def test_improperly_configured_servers(self):
        """Assert raise when settings are not empty but without `default`."""
        es_connections = connections.ConnectionHandler({}, {})

        indices = {
            'not_default': {}
        }

        handler = IndexHandler(es_connections, indices)

        with self.assertRaises(ImproperlyConfigured) as raised:
            # A simple call to servers must raise.
            handler.indices

        assert str(raised.exception) == "You must define a 'default' ElasticSearch index"
