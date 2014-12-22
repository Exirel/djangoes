"""Utility functions for testing purpose with ``djangoes``."""

def setup_djangoes():
    """Setup ElasticSearch connections with `̀ djangoes`̀  for testing purpose.

    When testing with ElasticSearch, used indices must not be the same as
    the one used for live settings, ie. tests must use the TEST settings.

    This function takes care of replacing each used index name by its
    appropriate test name.
    """
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
