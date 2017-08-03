"""
Manage the log file
"""

from datetime import datetime
import json
import os.path


class Logger(object):
    """Log file manager"""

    def __init__(self, path):
        """Set the path of the log file."""
        self._path = path
        self._need_write_to_log = True
        if os.path.isfile(path) is False:
            with open(path, 'a'):
                pass

    def save_operation(self, operation):
        """Save the operation to the log file."""
        operation['timestamp'] = str(datetime.now())
        line = json.dumps(operation)
        if self._need_write_to_log:
            with open(self._path, 'a') as log_file:
                log_file.write(line)
                log_file.write('\n')

    def restore_context(self, context):
        """Restore the context from the log file."""
        with open(self._path, 'r') as log_file:
            for line in log_file:
                operation = json.loads(line)
                operation.pop('timestamp', None)
                method = operation.pop("method")
                getattr(context, method)(**operation)

    def disable_logging(self):
        """Disable logging to the log file."""
        self._need_write_to_log = False

    def enable_logging(self):
        """Enable loggint to the log file."""
        self._need_write_to_log = True
