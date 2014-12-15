def pytest_configure(config):
    """
    Configure py.test to test with ES_SERVERS and ES_INDICES django settings.
    """
    from django.conf import settings
    settings.configure(ES_SERVERS={}, ES_INDICES={})
