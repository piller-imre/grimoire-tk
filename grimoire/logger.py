"""
Manage the log file
"""


class Logger(object):
    """Log file manager"""

    def __init__(self, path):
        """Set the path of the log file."""
        self._path = path

    def save_operation(self, operation):
        """Save the operation to the log file."""
        pass

    def restore_context(self, context):
        """Restore the context from the log file."""
        pass
