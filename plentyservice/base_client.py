"""The module for the base client other clients must implement."""

import abc

from .session_wrapper import SessionWrapper
from . import common
from .common import Cfg

# ABC compatible with Python 2 and 3
ABC = abc.ABCMeta("ABC", (object,), {"__slots__": ()})


class BaseClient(ABC):
    """A base client other clients must implement."""

    @staticmethod
    @abc.abstractmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        pass

    @abc.abstractmethod
    def build_commands(self):
        """Builds the commands for the client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        pass

    @abc.abstractmethod
    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        pass

    def get_authenticated_session(self):
        """
        Returns a requests Session that is preauthenticated and prepends the
        base_url
        Returns: a SessionWrapper
        """
        service_url = common.get_service_url(self.service_name())
        base_url = common.format_url_with_version(service_url, self.api_version())
        session = SessionWrapper(base_url, Cfg.get_plenty_api_key(), Cfg.get_plenty_api_secret())
        return session

    def head(self, path, **kwaargs):
        return self.get_authenticated_session().head(path, **kwaargs)

    def get(self, path, **kwargs):
        return self.get_authenticated_session().get(path, **kwargs)

    def post(self, path, **kwargs):
        return self.get_authenticated_session().post(path, **kwargs)

    def put(self, path, **kwargs):
        return self.get_authenticated_session().put(path, **kwargs)

    def patch(self, path, **kwargs):
        return self.get_authenticated_session().patch(path, **kwargs)

    def delete(self, path, **kwargs):
        return self.get_authenticated_session().delete(path, **kwargs)
