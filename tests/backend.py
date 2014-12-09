from djangoes.backends import Base


class ConnectionWrapper(Base):
    def __init__(self, alias, server, indices):
        Base.__init__(self, alias, server, indices)

    def configure_client(self):
        # Override to avoid the raise from Base class
        pass
