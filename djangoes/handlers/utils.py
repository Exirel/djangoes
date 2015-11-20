"""Utility functions for handlers."""
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured


def load_handler_class(handler_type, class_path):
    """Load the given ``handler_type`` from the given ``class_path``.

    :param string handler_type: Define the type of handler to load (connection,
        index, etc.). Used for logging purpose only.
    :param string class_path: A python import style path for a handler class.
    :raise ImproperlyConfigured: if the class can not be found at the given
        import location.

    It tries to import the class located at the given ``class_path``, or raise
    an ``ImproperlyConfigured`` exception. This is a convenient function to
    handle such common need: dynamic loading of a handler.
    """
    parts = class_path.split('.')
    handler_module, handler_class = '.'.join(parts[:-1]), parts[-1]

    try:
        return getattr(import_module(handler_module), handler_class)
    except (AttributeError, ImportError) as e_user:
        error_msg = ("%r isn't an available ElasticSearch %s.\n"
                     "Error was: %s" %
                     (class_path, handler_type, e_user))
        raise ImproperlyConfigured(error_msg)


def load_backend(backend_class_path):
    """Import and return the given connection backend class."""
    return load_handler_class('backend', backend_class_path)


def load_index(index_class_path):
    """Import and return the given index class."""
    return load_handler_class('index', index_class_path)
