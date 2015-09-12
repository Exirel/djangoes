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
    def create_connections_indices(self):
        """Create indices for all configured connections.

        Convenient method to create indices for all configured ElasticSearch
        connections.

        This method should be called during the setup of the test case.
        """
        index_names = set()

        for conn in connections.all():
            for index_name, index_settings in conn.get_indices_with_settings().items():
                if index_name not in index_names:
                    index_names.add(index_name)
                    conn.client.indices.create(index_name, index_settings)

    def delete_connections_indices(self):
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
                    conn.client.indices.delete(index_name)

    def create_connection_indices(self, conn):
        """Create indices for the given connection.

        Convenient method to create indices used by an ElasticSearch
        connection.

        This method should be called during the setup of the test case.
        """
        for index in conn.index_names:
            conn.client.indices.create(index)

    def delete_connection_indices(self, conn):
        """Delete indices for the given connection.

        Convenient method to delete indices used by an ElasticSearch
        connection.

        This method should be called during the tear down of the test case.
        """
        for index in conn.index_names:
            conn.client.indices.delete(index)
