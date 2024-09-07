"""
Abstract base class for instruments
"""

from abc import ABC, abstractmethod
from logging import Logger
import wrapt
import yaml
from yaml import SafeLoader


class Instrument(ABC):
    """
    Abstract class for instruments:
        - an instrument can be instanciated without opening it, opened and closed.
        - an instrument can be used asynchronously (non-blocking) or synchronously
        - an instrument can use user-supplied arguments from a YAML config file
        - an instrument can handle hot-plugging:
            - automatic detection of instrument disconnection
            - blocks ongoing operations and attempts to reconnect
    """

    def __init__(self, cfg_file_name: str, log: Logger):
        """
        Instrument initialization loads a YAML configuration file.
        """
        self._cfg_file_name: dict = cfg_file_name
        self._log: Logger = log
        self._cfg: dict = {}
        self._is_open: bool = False

        # Try to load custom params from YAML file
        # Raises an exception if fails
        try:
            with open(cfg_file_name, encoding="utf-8") as f:
                self._cfg = yaml.load(f, Loader=SafeLoader)
        except Exception as e:
            e.args += (
                f"Error while loading configuration file at '{cfg_file_name}'",
            )
            raise e

    def open(self):
        self._is_open = self._open()

    @abstractmethod
    def _open(self) -> bool:
        """
        Open and configure the instrument from the specified port.
        Returns `False` if the connection was not open.
        """
        pass

    def close(self) -> bool:
        was_open: bool = self._close()
        self._is_open = False
        return was_open

    @abstractmethod
    def _close(self) -> bool:
        """
        Close the communication with the instrument if needed.
        """
        pass

    def __del__(self):
        """
        Action to perform on class destruction.
        """
        self.close()

    def is_open(self) -> bool:
        return self._is_open

    @staticmethod
    @wrapt.decorator
    def retry_until_connected(_, instance, args, kwargs):
        """
        Wrapper for the instrument methods.
        Should only be used within this class or children of it.
        """
        success: bool = False
        result = None
        while not success:
            try:
                result = instance.wrapped(*args, **kwargs)
                success = True
            except TimeoutError:
                # A timeout occured: the instrument is considered disconnected
                instance._is_open = False  # pylint: disable=protected-access
                instance._log.warning(  # pylint: disable=protected-access
                    f"Instrument {__name__} disconnected, attempting reconnection..."
                )
                while not instance.is_open():
                    instance.open()
        return result
