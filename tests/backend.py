from djangoes.backends import Base


class ConnectionWrapper(Base):
    def configure_client(self):
        # Override to avoid the raise from Base class
        pass
