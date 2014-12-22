"""Tests runners for Django projects with ``djangoes``.

When using the built-in Django admin ``test`` command, the simplest way to
integrate ``djangoes`` is to configure the ``TEST_RUNNER`` settings, using the
runner provided by ``djangoes``::

    TEST_RUNNER = 'djangoes.test.runner.DiscoverRunner'

"""
from django.test.runner import DiscoverRunner as BaseRunner

from .utils import setup_djangoes


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
