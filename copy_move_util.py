import argparse
import os
from queue import Queue

from operations import operations


class CopyMove:
    """Minor utility for copying and moving files (also by mask) and folders.
    Attributes:
        parser: Argument parser that gets arguments from command line.
    """
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self._operation = None
        self._source_path = None
        self._destination_path = None
        self._threads_number = None

    @property
    def operation(self):
        """An operation that is going to be executed."""
        return self._operation

    @operation.setter
    def operation(self, command: str):
        self._operation = command

    @property
    def source_path(self):
        """An array of files' or folders' source paths."""
        return self._source_path

    @source_path.setter
    def source_path(self, args: dict):
        self._source_path = args

    @property
    def destination_path(self):
        """Destination path."""
        return self._destination_path

    @destination_path.setter
    def destination_path(self, args: dict):
        self._destination_path = args

    @property
    def threads_number(self):
        """Number of threads to use during an operation."""
        return self._threads_number

    @threads_number.setter
    def threads_number(self, args: dict):
        self._threads_number = args

    def get_arguments(self) -> None:
        """Gets arguments from command line."""
        self.parser.add_argument("-o", "--operation", help="Argument of operation")
        self.parser.add_argument("-f",
                                 "--from",
                                 nargs="+",
                                 help="Location from which you want to copy/move data")
        self.parser.add_argument("-t", "--to", help="Location where you want to copy/move data")
        self.parser.add_argument("--threads",
                                 default=1,
                                 help="Number of threads to be used during chosen operation")

        args = vars(self.parser.parse_args())
        self.parse_arguments(args)

    def parse_arguments(self, args: dict) -> None:
        """Parses arguments from command line into separate attributes."""
        self.operation = args['operation']
        self.source_path = args['from']
        for path in self.source_path:
            if not os.access(path, os.W_OK & os.X_OK):
                raise PermissionError('Not enough permissions for source path.')
        self.destination_path = args['to']
        if not os.access(self.destination_path, os.W_OK & os.X_OK):
            raise PermissionError('Not enough permissions for destination folder.')
        self.threads_number = int(args['threads'])

    def execute_command(self):
        """Finds appropriate command among a list of available commands and executes it."""
        if self.operation not in operations.keys():
            raise NameError('Operation not found')

        queue = Queue(maxsize=self.threads_number)
        operations[self.operation](
            queue,
            self.source_path,
            self.destination_path,
        )
