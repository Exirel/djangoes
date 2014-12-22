"""TestCase classes for ElasticSearch in Django.

These classes combine Django test case classes with djangoes mixin in order to
replace them in a Django project with ElasticSearch.

Instead of doing::

    from django.test.testcases import SimpleTestCase

One can do::

    from djangoes.test.testcases import SimpleTestCase

It works the same way for ``TransactionTestCase`` and ``TestCase``.
"""
from django.test.testcases import (
    SimpleTestCase as BaseSimpleTestCase,
    TransactionTestCase as BaseTransactionTestCase,
    TestCase as BaseTestCase)

from .mixins import ElasticSearchTestMixin


class SimpleTestCase(ElasticSearchTestMixin, BaseSimpleTestCase):
    """Simple test case with Django and ElasticSearch.

    Automatically create the indices for all configured ElasticSearch
    connections, combined with the setup & tear down of the Django
    ``SimpleTestCase`` test case class.
    """
    def _pre_setup(self):
        """Add creation of ES indices to pre-setup."""
        super()._pre_setup()
        self.create_connections_indices()

    def _post_teardown(self):
        """Add deletion of ES indices to post-tear down."""
        self.delete_connections_indices()
        super()._post_teardown()


class TransactionTestCase(ElasticSearchTestMixin, BaseTransactionTestCase):
    """Transaction test case with Django and ElasticSearch.

    Automatically create the indices for all configured ElasticSearch
    connections, combined with the setup & tear down of the Django
    ``TransactionTestCase`` test case class.
    """
    def _pre_setup(self):
        """Add creation of ES indices to pre-setup."""
        super()._pre_setup()
        self.create_connections_indices()

    def _post_teardown(self):
        """Add deletion of ES indices to post-tear down."""
        self.delete_connections_indices()
        super()._post_teardown()


class TestCase(ElasticSearchTestMixin, BaseTestCase):
    """Test case with Django and ElasticSearch.

    Automatically create the indices for all configured ElasticSearch
    connections, combined with the setup & tear down of the Django ``TestCase``
    test case class.
    """
    def _pre_setup(self):
        """Add creation of ES indices to pre-setup."""
        super()._pre_setup()
        self.create_connections_indices()

    def _post_teardown(self):
        """Add deletion of ES indices to post-tear down."""
        self.delete_connections_indices()
        super()._post_teardown()
