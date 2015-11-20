from unittest.case import TestCase
from unittest.mock import patch

from django.test.runner import DiscoverRunner as BaseRunner
from django.test.utils import override_settings

from djangoes.test.runner import DiscoverRunner, setup_djangoes


class TestSetupDjangoesFunctions(TestCase):
    """Assert how should behave the ``setup_djangoes`` function.

    This function is the most important part of the test suite using Django and
    ElasticSearch, as it will perform manipulation of the settings in order to
    avoid race condition with tests using a real index already used at the same
    time for its initial purpose.
    """

    # Assertions about indices, index_names and alias_names.
    # ======================================================

    def test_setup_elasticsearch_indices(self):
        """Assert indices are replaced by test values."""
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

    def test_setup_elasticsearch_indices_with_aliases(self):
        """Assert indices are replaced by test values."""
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
                'ALIASES': ['alias_backup']
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_indices = ['index_prod', 'alias_backup']
            assert sorted(conn.indices) == sorted(expected_indices)

            setup_djangoes()

            expected_indices = sorted(['index_prod_test',
                                       'alias_backup_test'])
            assert sorted(conn.indices) == expected_indices

    def test_setup_elasticsearch_index_names(self):
        """Assert index names are replaced by test values."""
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
            expected_names = ['index_prod', 'index_prod_backup']
            assert sorted(conn.index_names) == sorted(expected_names)

            setup_djangoes()

            expected_names = sorted(['index_prod_test',
                                     'index_prod_backup_test'])
            assert sorted(conn.index_names) == expected_names

    def test_setup_elasticsearch_index_names_with_aliases(self):
        """Assert index names are replaced by test values even with aliases."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['test_index_1', 'test_index_2']
            }
        }
        indices = {
            'test_index_1': {
                'NAME': 'index_prod',
                'ALIASES': ['alias_prod']
            },
            'test_index_2': {
                'NAME': 'index_prod_backup',
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_names = ['index_prod', 'index_prod_backup']
            assert sorted(conn.index_names) == sorted(expected_names)

            setup_djangoes()

            expected_names = sorted(['index_prod_test',
                                     'index_prod_backup_test'])
            assert sorted(conn.index_names) == expected_names

    def test_setup_elasticsearch_alias_names(self):
        """Assert alias names are replaced by test values."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['test_index_1', 'test_index_2']
            }
        }
        indices = {
            'test_index_1': {
                'NAME': 'index_prod',
                'ALIASES': ['alias_prod']
            },
            'test_index_2': {
                'NAME': 'index_prod_backup',
                'ALIASES': ['alias_prod_backup']
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            expected_names = ['alias_prod', 'alias_prod_backup']
            assert sorted(conn.alias_names) == sorted(expected_names)

            setup_djangoes()

            expected_names = sorted(['alias_prod_test',
                                     'alias_prod_backup_test'])
            assert sorted(conn.alias_names) == expected_names

    def test_setup_elasticsearch_settings(self):
        """Assert index test settings are get from initial values."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['test_index']
            }
        }
        indices = {
            'test_index': {
                'NAME': 'index_prod',
                'ALIASES': ['alias_prod'],
                'SETTINGS': {
                    'index': {
                        'number_of_replicas': 1
                    }
                }
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            index_settings = conn.get_indices_with_settings()

            assert 'index_prod' in index_settings
            assert index_settings['index_prod'] == {
                'index': {
                    'number_of_replicas': 1
                }
            }

            setup_djangoes()

            index_settings = conn.get_indices_with_settings()

            assert 'index_prod' not in index_settings
            assert 'index_prod_test' in index_settings
            assert index_settings['index_prod_test'] == {
                'index': {
                    'number_of_replicas': 1
                }
            }

    def test_setup_elasticsearch_settings_with_settings(self):
        """Assert index settings are replaced by test values."""
        servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper',
                'INDICES': ['test_index']
            }
        }
        indices = {
            'test_index': {
                'NAME': 'index_prod',
                'ALIASES': ['alias_prod'],
                'SETTINGS': {
                    'index': {
                        'number_of_replicas': 1
                    }
                },
                'TEST': {
                    'SETTINGS': {
                        'index': {
                            'number_of_replicas': 0
                        }
                    },
                }
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            index_settings = conn.get_indices_with_settings()

            assert 'index_prod' in index_settings
            assert index_settings['index_prod'] == {
                'index': {
                    'number_of_replicas': 1
                }
            }

            setup_djangoes()

            index_settings = conn.get_indices_with_settings()

            assert 'index_prod' not in index_settings
            assert 'index_prod_test' in index_settings
            assert index_settings['index_prod_test'] == {
                'index': {
                    'number_of_replicas': 0
                }
            }

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

            expected_indices = ['index_test']
            assert conn.indices == expected_indices
            assert conn_copy.indices == expected_indices

    # Assertions about global override.
    # =================================

    def test_setup_elasticsearch_global_override_indices(self):
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

    def test_setup_elasticsearch_global_override_aliases(self):
        """Assert server test settings can override globally test aliases."""
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
                'ALIASES': ['alias_prod']
            },
            'override': {
                'NAME': 'overridden',
                'ALIASES': ['alias_overridden']
            }
        }

        with override_settings(ES_SERVERS=servers, ES_INDICES=indices):
            from djangoes import connections

            conn = connections['default']
            assert conn.indices == ['alias_prod']

            setup_djangoes()

            assert conn.indices == ['alias_overridden_test']

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
