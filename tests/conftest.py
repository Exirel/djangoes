def pytest_configure(config):
    """Configure py.test with ES_SERVERS and ES_INDICES django settings."""
    from django.conf import settings

    settings.configure(ES_SERVERS={}, ES_INDICES={})


def pytest_runtest_setup(item):
    """Reset djangoes singleton.

    Before each test, reset the singleton `djangoes.connections` to its initial
    value, ie. an empty instance of djangoes.ConnectionHandler.
    """
    import djangoes
    from djangoes import ConnectionHandler

    djangoes.connections = ConnectionHandler()
