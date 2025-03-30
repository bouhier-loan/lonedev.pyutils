"""Logger module for projects using rich library."""
import os

from lonedev.globalargs import FlagType, GlobalArgs
from lonedev.logger.logger import Logger

if not os.path.exists('logs'):
    os.makedirs('logs')

GlobalArgs.add_argument(
    "--debug",
    name="debug_enabled",
    flag_type=FlagType.TRUE,
    help_message="Enable debug mode",
)

GlobalArgs.add_argument(
    "--log-file",
    name="log_file",
    flag_type=FlagType.VALUE,
    help_message="Path to the log file",
    default="",
)

GlobalArgs.add_argument(
    "--disable-file-logging",
    name="file_logging_enabled",
    flag_type=FlagType.FALSE,
    help_message="Disable file logging",
)

__all__ = ["Logger"]
