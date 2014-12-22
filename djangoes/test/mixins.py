"""TestCase Mixin classes for ElasticSearch in Django.

These Mixin classes can be combined with Django TestCase in order to make
assertion when using ElasticSearch in the tested code.
"""
from djangoes import connections


class ElasticSearchTestMixin(object):
    """Expose public methods to set up and tear down testing environment.

    This mixin must be combined with a TestCase and its methods should be used
    in the set-up/tear down process of test cases.
    """
    @classmethod
    def create_connections_indices(cls):
        """Create indices for all configured connections.

        Convenient method to create indices for all configured ElasticSearch
        connections.

        This method should be called during the setup of the test case.
        """
        index_names = set()

        for conn in connections.all():
            for index_name in conn.index_names:
                if index_name not in index_names:
                    index_names.add(index_name)
                    conn.meta.indices.create(index_name)

    @classmethod
    def delete_connections_indices(cls):
        """Delete indices for all configured connections.

        Convenient method to delete indices for all configured ElasticSearch
        connections.

        This method should be called during the tear down of the test case.
        """
        index_names = set()

        for conn in connections.all():
            for index_name in conn.index_names:
                if index_name not in index_names:
                    index_names.add(index_name)
                    conn.meta.indices.delete(index_name)

    @classmethod
    def create_connection_indices(cls, conn):
        """Create indices for the given connection.

        Convenient method to create indices used by an ElasticSearch
        connection.

        This method should be called during the setup of the test case.
        """
        for index in conn.index_names:
            conn.meta.indices.create(index)

    @classmethod
    def delete_connection_indices(cls, conn):
        """Delete indices for the given connection.

        Convenient method to delete indices used by an ElasticSearch
        connection.

        This method should be called during the tear down of the test case.
        """
        for index in conn.index_names:
            conn.meta.indices.delete(index)
