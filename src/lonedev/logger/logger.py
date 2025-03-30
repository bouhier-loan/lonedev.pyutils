"""Logger module for logging messages with different severity levels."""

import datetime

from rich import console

from lonedev.globalargs import GlobalArgs


class Logger:
    """Logger class for logging messages with different severity levels."""

    _max_prefix_length: int = 0
    _log_file_path: str = ""
    _file_logging_enabled: bool = False
    _debug_enabled: bool = False
    _console = console.Console(log_path=False)

    _log_file: str
    _initialized: bool = False

    _prefix: str = "Global"

    def __init__(self, name: str) -> None:
        """Create a new instance of the class if it does not exist."""
        if not Logger._initialized:
            Logger._log_file_path = (
                f"logs/{GlobalArgs()["log_file"]}"
                if GlobalArgs()["log_file"] != ""
                else f"logs/{
                    datetime.datetime.now(tz=datetime.UTC).strftime('%Y-%m-%d_%H-%M-%S')
                }.log"
            )
            Logger._debug_enabled = GlobalArgs()["debug_enabled"]
            Logger._file_logging_enabled = GlobalArgs()["file_logging_enabled"]
            Logger._initialized = True

        self._prefix = name
        if Logger._max_prefix_length < len(self._prefix):
            Logger._max_prefix_length = len(self._prefix)


    def _log(self, message: str, level: str, level_color: str) -> None:
        """
        Log a message with a specific severity level.

        :param message: Message to log
        :param level: Severity level of the message
        :param level_color: Color for the severity level
        :return: None
        """
        Logger._max_prefix_length = max(Logger._max_prefix_length, len(self._prefix))

        if Logger._file_logging_enabled:
            with open(Logger._log_file_path, "a") as log_file:
                log_file.write(
                    f"[{
                        datetime.datetime.now(tz=datetime.UTC).strftime(
                            '%Y-%m-%d_%H-%M-%S'
                        )
                    } "
                    f"[{level.upper()}] "
                    f"{self._prefix} - "
                    f"{message}"
                    f"\n",
                )

        Logger._console.log(
            f"[[{level_color}]{level.upper()}[/{level_color}]]",
            f"{' ' * (8 - len(level))}"
            f"[grey50]{self._prefix}[/grey50]"
            f"{' ' * (Logger._max_prefix_length - len(self._prefix) + 1)}-",
            message,
        )

    def log(self, message: str) -> None:
        """
        Log a message with the INFO severity level.

        :param message: Message to log
        :return: None
        """
        self._log(message, "info", "blue")

    def debug(self, message: str) -> None:
        """
        Log a message with the DEBUG severity level.

        :param message: Message to log
        :return: None
        """
        if Logger._debug_enabled:
            self._log(message, "debug", "green")

    def warning(self, message: str) -> None:
        """
        Log a message with the WARNING severity level.

        :param message: Message to log
        :return: None
        """
        self._log(message, "warning", "yellow")

    def error(self, message: str) -> None:
        """
        Log a message with the ERROR severity level.

        :param message: Message to log
        :return: None
        """
        self._log(message, "error", "red")
