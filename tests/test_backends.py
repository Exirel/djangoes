from unittest.case import TestCase

from djangoes.backends.abstracts import Base


class TestBase(TestCase):
    """Make assertions about the behavior of bakends.Base."""

    def test_configure_client_not_implemented(self):
        """The Base class is only an abstract class."""
        backend = Base('test_backend', {}, {})

        with self.assertRaises(NotImplementedError):
            backend.configure_client()

    # Assertions on indices property
    # ==============================

    def test_indices(self):
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': []
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert backend.indices == ['index1']

    def test_indices_with_aliases(self):
        """The purpose of indices is to get names to use into queries."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert sorted(backend.indices) == ['alias1', 'alias2']

    def test_indices_with_multiple_indices_and_aliases(self):
        """And to get only aliases when used, and index name if no alias."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
            'test_name_2': {
                'NAME': 'index2',
                'ALIASES': ['alias1']
            },
            'test_name_3': {
                'NAME': 'index3',
                'ALIASES': []
            }
        }

        backend = Base('test_backend', {}, test_indices)

        assert sorted(backend.indices) == ['alias1', 'alias2', 'index3']

    # Assertions on index_names property
    # ==================================

    def test_index_names(self):
        """Assert index_names return the list of configured indices."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': []
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert backend.index_names == ['index1']

    def test_index_names_with_aliases(self):
        """The purpose of index_names is to get only indices, not aliases."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert backend.index_names == ['index1']

    def test_index_names_with_multiple_indices_and_aliases(self):
        """And index_names gets names from all indices."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
            'test_name_2': {
                'NAME': 'index2',
                'ALIASES': ['alias1']
            },
            'test_name_3': {
                'NAME': 'index3',
                'ALIASES': []
            }
        }

        backend = Base('test_backend', {}, test_indices)

        assert sorted(backend.index_names) == ['index1', 'index2', 'index3']

    # Assertions on alias_names property
    # ==================================

    def test_alias_names(self):
        """Assert alias_names return the list of configured aliases."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1']
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert backend.alias_names == ['alias1']

    def test_alias_names_no_alias(self):
        """The purpose of alias_names is to get only aliases, not indices."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': []
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert backend.alias_names == []

    def test_alias_names_with_multiple_aliases(self):
        """And we can have multiple aliases from one index."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert sorted(backend.alias_names) == ['alias1', 'alias2']

    def test_alias_names_with_multiple_indices(self):
        """Assert multiple aliases from multiple indices without duplicate."""
        test_indices = {
            'test_name_1': {
                'NAME': 'index1',
                'ALIASES': ['alias1', 'alias2']
            },
            'test_name_2': {
                'NAME': 'index2',
                'ALIASES': ['alias3']
            },
            'test_name_3': {
                'NAME': 'index3',
                'ALIASES': ['alias1']
            },
        }

        backend = Base('test_backend', {}, test_indices)

        assert sorted(backend.alias_names) == ['alias1', 'alias2', 'alias3']
