from unittest.case import TestCase
from unittest.mock import patch

from django.test.runner import DiscoverRunner as BaseRunner
from django.test.utils import override_settings

from djangoes.test.runner import DiscoverRunner, setup_djangoes


class TestSetupDjangoesFunctions(TestCase):
    def test_setup_elasticsearch(self):
        """Assert indices and index names are replaced by test values."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['test_index_1', 'test_index_2']
            }
        }
        indices = {
            'test_index_1': {
                'NAME': 'index_prod',
            },
            'test_index_2': {
                'NAME': 'index_prod_backup',
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_indices = ['index_prod', 'index_prod_backup']
            assert sorted(conn.indices) == sorted(expected_indices)

            setup_djangoes()

            expected_indices = sorted(['index_prod_test',
                                       'index_prod_backup_test'])
            assert sorted(conn.indices) == expected_indices

    def test_setup_elasticsearch_global_override(self):
        """Assert server test settings can override globally test indices."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index'],
                'TEST': {
                    'INDICES': ['override']
                }
            }
        }
        indices = {
            'index': {
                'NAME': 'index_prod',
            },
            'override': {
                'NAME': 'overridden',
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_indices = ['index_prod']
            assert sorted(conn.indices) == sorted(expected_indices)

            setup_djangoes()

            expected_indices = sorted(['overridden_test'])
            assert sorted(conn.indices) == expected_indices

    def test_setup_elasticsearch_no_test_indices(self):
        """Assert tests can not be set up when settings are invalid.

        Each server connection must provide either a list of indices, or a test
        settings with a list of indices to use for tests.
        """
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': [],
                'TEST': {
                    'INDICES': []
                }
            }
        }
        indices = {}

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            assert conn.indices == []

            with self.assertRaises(RuntimeError):
                setup_djangoes()

    def test_setup_elasticsearch_reuse_index(self):
        """Assert indices and index names are replaced by test values.

        In this case, we want to be sure that two connections can access the
        same index, and that the configuration of one won't cause any issue.
        """
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index']
            },
            'copy' : {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index']
            }
        }
        indices = {
            'index': {
                'NAME': 'index_prod',
                'TEST': {
                    'NAME': 'index_test'
                }
            },
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            setup_djangoes()

            conn = connections['default']
            conn_copy = connections['copy']

            expected_indices = sorted(['index_test'])
            assert sorted(conn.indices) == expected_indices
            assert sorted(conn_copy.indices) == expected_indices

    def test_setup_elasticsearch_global_override_reuse_index(self):
        """Assert server test settings can override globally test indices."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index'],
                'TEST': {
                    'INDICES': ['override']
                }
            },
            'copy': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index'],
                'TEST': {
                    'INDICES': ['override']
                }
            }
        }
        indices = {
            'index': {
                'NAME': 'index_prod',
            },
            'override': {
                'NAME': 'overridden',
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            setup_djangoes()
            conn = connections['default']
            conn_copy = connections['copy']

            expected_indices = sorted(['overridden_test'])
            assert conn.indices == expected_indices
            assert conn_copy.indices == expected_indices


class TestDiscoverRunner(TestCase):
    @patch.object(BaseRunner, 'setup_test_environment')
    def test_setup_test_environment(self, base_setup_method):
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['index'],
                'TEST': {
                    'INDICES': ['override']
                }
            }
        }
        indices = {
            'index': {
                'NAME': 'index_prod',
            },
            'override': {
                'NAME': 'overridden',
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_indices = ['index_prod']
            assert sorted(conn.indices) == sorted(expected_indices)

            # Use the method from djangoes's test runner
            runner = DiscoverRunner()
            runner.setup_test_environment()

            expected_indices = sorted(['overridden_test'])
            assert sorted(conn.indices) == expected_indices

        # The runner must call the parent method once.
        base_setup_method.assert_called_once_with()
