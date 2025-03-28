"""Module to manage global arguments for command lines."""

import argparse
from enum import StrEnum
from typing import Any


class FlagType(StrEnum):
    """Enum class for flag types."""

    VALUE = ("store",)
    """Flag with a value (e.g., --flag value)"""
    TRUE = ("store_true",)
    """The flag is true when present, false otherwise (e.g., --flag)"""
    FALSE = ("store_false",)
    """The flag is false when present, true otherwise (e.g., --no-flag)"""


class GlobalArgs:
    """Singleton class to manage global arguments for command lines."""

    _instance = None
    _parser = None
    parsed_args: argparse.Namespace = None

    def __new__(cls) -> "GlobalArgs":
        """Create a new instance of the class if it does not exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._parser = argparse.ArgumentParser()
        return cls._instance

    @classmethod
    def add_argument(
        cls,
        *flags: str,
        name: str,
        flag_type: FlagType = FlagType.VALUE,
        help_message: str | None = None,
        default: Any = None,
    ) -> None:
        """
        Add an argument to the global argument parser.

        :param flags: Flags for the argument
        :param name: Name of the argument
        :param flag_type: Type of the flag (FlagType enum)
        :param help_message: Help message for the flag
        :param default: Default value for the flag
        :return: None
        """
        if flag_type == FlagType.VALUE:
            cls()._parser.add_argument(
                *flags,
                dest=name,
                action=flag_type.value,
                help=help_message,
                default=default,
            )
        else:
            cls()._parser.add_argument(
                *flags,
                dest=name,
                action=flag_type.value,
                help=help_message,
            )

    @classmethod
    def _parse_args(cls) -> argparse.Namespace:
        """
        Parse the global arguments.

        :return: argparse.Namespace
        """
        cls().parsed_args = cls()._parser.parse_args()
        return cls().parsed_args

    @classmethod
    def __iter__(cls) -> argparse.Namespace:
        """Return the parsed arguments."""
        cls._parse_args()
        return cls().parsed_args

    @classmethod
    def __getitem__(cls, key: str) -> Any:
        """Return the value of the argument with the given key."""
        cls._parse_args()
        return getattr(cls().parsed_args, key)

    @classmethod
    def __class_getitem__(cls, item) -> Any:
        return cls[item]
