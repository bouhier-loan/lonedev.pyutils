from lonedev.globalargs.global_args import GlobalArgs, FlagType
from rich.console import Console
from rich.table import Table
from rich.pager import Pager
import os
import time

class LoggerCLI:
    """Logger class for logging messages with different severity levels."""

    _console = Console()

    def __init__(self) -> None:
        """Create a new instance of the class if it does not exist."""
        pass

    def print_welcome(self) -> None:
        """
        Print a welcome message.

        :return: None
        """
        self._console.print("""
 _                              _                _
| |                            | |              | |
| |      ___   _ __    ___   __| |  ___ __   __ | |      ___    __ _   __ _   ___  _ __
| |     / _ \ | '_ \  / _ \ / _` | / _ \\ \ / / | |     / _ \  / _` | / _` | / _ \| '__|
| |____| (_) || | | ||  __/| (_| ||  __/ \ V /  | |____| (_) || (_| || (_| ||  __/| |
\_____/ \___/ |_| |_| \___| \__,_| \___|  \_/   \_____/ \___/  \__, | \__, | \___||_|
                                                                __/ |  __/ |
                                                               |___/  |___/
        """)

        self._console.print("Welcome to the Logger CLI. Use the following commands to interact with the logger:")
        self._console.print("log - Retrieve logs with the specified severity level from the last log file")
        self._console.print("\tOptions: -f, --file <file> - Specify a log file to retrieve logs from")
        self._console.print("\t\t\t-s, --severity <severity> - Specify a severity level to retrieve logs from (all, debug, info, warning, error)")

        self._console.print("list - List all log files")
        self._console.print("recap - Recap all logs")
        self._console.print("clear <number?> - Clear the specified number of logs (default: all)")

    def call(self, action: str, args: list) -> None:
        """
        Call the specified action with the given arguments.

        :param action: Action to perform
        :param args: Arguments for the action
        :return: None
        """
        if action == "log":
            self.log()
        elif action == "list":
            self.list()
        elif action == "recap":
            self.recap()
        elif action == "clear":
            self.clear(args)
        else:
            self.print_welcome()

    @staticmethod
    def _parse_line(line: str) -> dict[str, str]:
        """
        Parse a log line.

        :param line: Line to parse
        :return: Parsed line
        """

        # Split the line into parts
        timestamp = line[1:20]
        severity = line[22:].split(" ")[0].removeprefix("[").removesuffix("]")
        prefix = line.split(" - ")[0].split(" ")[-1]
        message = line.split(" - ")[1]

        return {
            "timestamp": timestamp,
            "severity": severity,
            "prefix": prefix,
            "message": message
        }

    @staticmethod
    def clear(args: list) -> None:
        """
        Clear the specified number of log files.

        :param args: Arguments for the action
        :return: None
        """
        if len(args) == 0:
            files = os.listdir( f"{os.path.abspath(".")}\\logs" )
            for file in files:
                os.remove(f"{os.path.abspath(".")}\\logs\\{file}")
        else:
            for i in range(int(args[0])):
                files = os.listdir( f"{os.path.abspath(".")}\\logs" )
                os.remove(f"{os.path.abspath(".")}\\logs\\{files[i]}")

    def list(self) -> None:
        """
        List all log files.

        :return: None
        """
        files = os.listdir( f"{os.path.abspath(".")}\\logs" )

        table = Table(title="Log Files")
        table.add_column("File Name")
        table.add_column("Size")
        table.add_column("Last Modified")

        for file in files:
            file_path = f"{os.path.abspath(".")}\\logs\\{file}"

            # Get human readable size (KB, MB, GB, etc.)
            size = os.path.getsize(file_path)
            size_name = ("B", "KB", "MB", "GB", "TB")
            i = int(0)
            while size > 1024 and i < len(size_name)-1:
                size = size/1024
                i += 1
            size = f"{size:.2f} {size_name[i]}"

            # Get human readable last modified time
            last_modified = time.ctime(os.path.getmtime(file_path))


            table.add_row(file, size, last_modified)

        self._console.print(table)

    def log(self) -> None:
        """
        Retrieve logs with the specified severity level.

        :param args: Arguments for the action
        :return: None
        """
        severity = GlobalArgs()["severity"].upper()
        file = GlobalArgs()["file"]

        level_colors = {
            "DEBUG": "blue",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red"
        }

        if file == "latest":
            file = os.listdir( f"{os.path.abspath(".")}\\logs" )[-1]

        with open(f"{os.path.abspath(".")}\\logs\\{file}", "r") as log_file:
            lines = log_file.readlines()
            last_line_severity = None
            with self._console.pager(styles=True) as pager:
                for line in lines:
                    if line.startswith("["):
                        parsed_line = self._parse_line(line)
                        last_line_severity = parsed_line["severity"]
                        if severity == "ALL" or severity == parsed_line["severity"]:
                            prefix = parsed_line["prefix"]
                            if len(prefix) > 9:
                                prefix = prefix[:6] + "... "

                            self._console.print(
                                f"[grey50][{parsed_line['timestamp']}][/grey50] "
                                f"[{level_colors[parsed_line['severity']]}][{parsed_line['severity'].upper()}][/{level_colors[parsed_line['severity']]}]"
                                f"{' ' * (8 - len(parsed_line['severity']))}"
                                f"[grey50]{prefix}[/grey50]"
                                f"{' ' * (10 - len(parsed_line['prefix']))}"
                                f"- {parsed_line['message']}"
                            )
                    else:
                        if severity == "ALL" or severity == last_line_severity:
                            self._console.print(line)

    def recap(self) -> None:
        """
        Recap all logs.

        :return: None
        """
        files = os.listdir( f"{os.path.abspath(".")}\\logs" )

        warnings = {}
        errors = {}
        tot_warnings = 0
        tot_errors = 0

        for file in files:
            with open(f"{os.path.abspath(".")}\\logs\\{file}", "r") as log_file:
                lines = log_file.readlines()
                for line in lines:
                    if line.startswith("["):
                        parsed_line = self._parse_line(line)
                        if parsed_line["severity"] == "WARNING":
                            if file not in warnings:
                                warnings[file] = {
                                    "processes": {},
                                    "total": 0
                                }

                            if parsed_line["prefix"] not in warnings[file]["processes"]:
                                warnings[file]["processes"][parsed_line["prefix"]] = 0

                            warnings[file]["processes"][parsed_line["prefix"]] += 1
                            warnings[file]["total"] += 1
                            tot_warnings += 1

                        elif parsed_line["severity"] == "ERROR":
                            if file not in errors:
                                errors[file] = {
                                    "processes": {},
                                    "total": 0
                                }

                            if parsed_line["prefix"] not in errors[file]["processes"]:
                                errors[file]["processes"][parsed_line["prefix"]] = 0

                            errors[file]["processes"][parsed_line["prefix"]] += 1
                            errors[file]["total"] += 1
                            tot_errors += 1

        table = Table(title="Recap")
        table.add_column("File Name")
        table.add_column("Process Name")
        table.add_column("Total Warnings")
        table.add_column("Total Errors")

        for file in files:
            file_warnings = warnings[file]["total"] if file in warnings else 0
            file_errors = errors[file]["total"] if file in errors else 0

            if file_warnings > 0 or file_errors > 0:
                processes = {}
                for process in warnings[file]["processes"]:
                    processes[process] = {
                        "warnings": warnings[file]["processes"][process],
                        "errors": 0
                    }

                for process in errors[file]["processes"]:
                    if process in processes:
                        processes[process] = {
                            "warnings": 0,
                            "errors": errors[file]["processes"][process]
                        }
                    else:
                        processes[process] = {
                            "warnings": 0,
                            "errors": errors[file]["processes"][process]
                        }

                for process in processes:
                    table.add_row(file, process, str(processes[process]["warnings"]), str(processes[process]["errors"]))

            table.add_row("", "Total.", str(file_warnings), str(file_errors))
            table.add_row("", "", "", "")

        table.add_section()
        table.add_row("Total", "", str(tot_warnings), str(tot_errors))

        self._console.print(table)



def app():
    parser = GlobalArgs.get_parser()
    parser.add_argument("action", nargs="?", help="Action to perform", choices=["log", "list", "recap", "clear"],
                        default="")
    parser.add_argument("args", nargs="*", help="Arguments for the action", default=[])
    GlobalArgs().add_argument("-s", "--severity", name="severity", flag_type=FlagType.VALUE, help_message="Severity level to retrieve logs from (all, debug, info, warning, error)", default="all")
    GlobalArgs().add_argument("-f", "--file", name="file", flag_type=FlagType.VALUE, help_message="Log file to retrieve logs from", default="latest")

    LoggerCLI().call(GlobalArgs()["action"], GlobalArgs()["args"])
