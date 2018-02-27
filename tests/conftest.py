def pytest_configure(config):
    """Configure Django with ``ES_SERVERS`` and ``ES_INDICES`` settings."""
    from django.conf import settings

    settings.configure(ES_SERVERS={}, ES_INDICES={})


def pytest_runtest_setup(item):
    """Reset djangoes singleton.

    Before each test, reset the singleton ``djangoes.connections`` to its
    initial value, ie. an empty instance of
    :class:`djangoes.handler.connections.ConnectionHandler`.
    """
    import djangoes

    djangoes.indices = djangoes.IndexHandler(djangoes.ConnectionHandler())
    djangoes.connections = djangoes.indices.connections
