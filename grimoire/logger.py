"""
Manage the log file
"""

import json

from grimoire.context import Context


class Logger(object):
    """Log file manager"""

    def __init__(self, path):
        """Set the path of the log file."""
        self._path = path

    def save_operation(self, operation):
        """Save the operation to the log file."""
        line = json.dumps(operation)
        with open(self._path, 'a') as log_file:
            log_file.write(line)

    def restore_context(self):
        """Restore the context from the log file."""
        context = Context()
        with open(self._path, 'r') as log_file:
            for line in log_file:
                print(line)
        return context
