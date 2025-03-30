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

    _instance: "Logger" = None
    _log_file: str

    prefix: str = "Global"
    """Prefix for log messages."""

    def __new__(cls) -> "Logger":
        """Create a new instance of the class if it does not exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._log_file_path = (
                GlobalArgs()["log_file"]
                if GlobalArgs()["log_file"] != ""
                else f"logs/{datetime.datetime.now().astimezone().isoformat()[:-6]}.log"
            )
            cls._debug_enabled = GlobalArgs()["debug_enabled"]
            cls._file_logging_enabled = GlobalArgs()["file_logging_enabled"]
        return cls._instance

    @classmethod
    def get_logger(cls, prefix: str) -> "Logger":
        """
        Get a logger instance with a specific prefix.

        :param prefix: Prefix for the logger
        :return: Logger instance
        """
        logger = cls()
        logger.prefix = prefix
        cls._max_prefix_length = max(cls._max_prefix_length, len(prefix))
        return logger

    def _log(self, message: str, level: str, level_color: str) -> None:
        """
        Log a message with a specific severity level.

        :param message: Message to log
        :param level: Severity level of the message
        :param level_color: Color for the severity level
        :return: None
        """
        Logger._max_prefix_length = max(Logger._max_prefix_length, len(self.prefix))

        if Logger._file_logging_enabled:
            with open(Logger._log_file_path, "a") as log_file:
                log_file.write(
                    f"[{
                        datetime.datetime.now(tz=datetime.UTC)
                        .astimezone()
                        .isoformat()[:-6]
                    } "
                    f"[{level.upper()}] "
                    f"{self.prefix} - "
                    f"{message}"
                    f"\n",
                )

        Logger._console.log(
            f"[[{level_color}]{level.upper()}[/{level_color}]]",
            f"{' ' * (8 - len(level))}"
            f"[grey50]{self.prefix}[/grey50]"
            f"{' ' * (Logger._max_prefix_length - len(self.prefix) + 1)}-",
            message,
        )
