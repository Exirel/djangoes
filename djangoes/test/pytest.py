"""Py.test plugin for ``djangoes`` and ``pytest-django``.

Allow to use ``py.test`` and ElasticSearch for testing purpose of a Django
project. It requires the ``py.test`` plugin ``pytest-django``, but won't fail
without: if the plugin is not installed this one won't try to setup the tests
environment, and consider it has nothing to do.

The current version is quite simple as it setups only the ElasticSearch
connections, and it does not provide fixture nor specific helper.
"""
import pytest

from .utils import setup_djangoes


# Requires the pytest-django plugin in order to work.
pytest_plugins = 'pytest_django.plugin'  #pylint: disable=invalid-name


def django_settings_is_configured():
    """Return True if Django settings are configured.

    Try to import and use ``django_settings_is_configured`` function from the
    ``pytest_django`` py.test plugin, otherwise return always False.

    This should never happen as this plugin requires pytest_django."""
    try:
        #pylint: disable=redefined-outer-name
        from pytest_django.lazy_django import django_settings_is_configured
        return django_settings_is_configured()
    except ImportError:
        pass

    return False


#pylint: disable=unused-argument
@pytest.fixture(autouse=True, scope="session")
def _djangoes_test_environment(request):
    """Ensure that Django is loaded and has its testing environment setup.

    As this plugin requires the pytest-django plugin, it uses the same mecanism
    to setup django environment.
    """
    if django_settings_is_configured():
        setup_djangoes()
