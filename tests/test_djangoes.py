import unittest


class TestProxyConnectionHandler(unittest.TestCase):
    def test_attributes(self):
        # Local import to manipulate elements
        from djangoes import connections, connection

        connections._servers = {
            'default': {
                'ENGINE': 'tests.backend.ConnectionWrapper'
            }
        }
        connections._indices = {}

        # Existing attribute.
        assert connection.alias == 'default'

        # New attribute.
        assert not hasattr(connection, 'new_attribute')

        connections['default'].new_attribute = 'test_value'

        assert hasattr(connection, 'new_attribute')
        assert connection.new_attribute == 'test_value'

        del connection.new_attribute

        assert not hasattr(connection, 'new_attribute')
        assert not hasattr(connections['default'], 'new_attribute')

        connection.new_attribute = 'test_new_attribute_again'

        assert hasattr(connection, 'new_attribute')
        assert hasattr(connections['default'], 'new_attribute')

        assert connection == connections['default']
        assert not (connection != connections['default'])
