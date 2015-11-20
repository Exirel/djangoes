"""All exceptions classes for djangoes."""

class ConnectionDoesNotExist(KeyError):
    """Specific type of KeyError when a connection does not exist."""
    pass


class IndexDoesNotExist(KeyError):
    """Specific type of KeyError when an index does not exist."""
    pass
