from django.test.runner import DiscoverRunner as BaseRunner


def setup_djangoes():
    """Setup ElasticSearch connection with djangoes for testing purpose.

    When testing with ElasticSearch, used indices must not be the same as
    the one used for live settings, ie. tests must use the TEST settings."""
    from djangoes import connections

    for alias in connections:
        # Get the connection object.
        conn = connections[alias]

        server_test_indices = conn.server['TEST']['INDICES']
        if server_test_indices:
            # Update list of indices.
            conn.server.update({
                'INDICES': server_test_indices
            })
            # Refresh connection's indices settings
            conn.server_indices = connections.get_server_indices(conn.server)

        elif not conn.server_indices:
            raise RuntimeError(
                'Improperly configured settings for ElasticSearch \'%s\' '
                'connection: either configure a list of indices or a list of '
                'indices for testing purpose.' % alias)

        # Replace each index by its test settings.
        for indices in conn.server_indices.values():
            indices.update({
                'NAME': indices['TEST']['NAME'],
                'ALIASES': indices['TEST']['ALIASES']
            })

        # Refresh connection's cached properties.
        conn.indices = conn.get_indices()
        conn.index_names = conn.get_index_names()


class DiscoverRunner(BaseRunner):
    """Unittest Runner with Django and ElasticSearch.

    Setup ElasticSearch connections in order to run tests with the test
    settings and not the developement/production settings.

    When using djangoes in a Django project, it requires to define the settings
    option `TEST_RUNNER` to `djangoes.test.runner.DjangoesDiscoverRunner` to
    allow the tests with djangoes and ElasticSearch to work properly.
    """
    def setup_test_environment(self, **kwargs):
        super(DiscoverRunner, self).setup_test_environment(**kwargs)
        setup_djangoes()
