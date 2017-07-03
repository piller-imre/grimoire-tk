"""
Storage class definition
"""


class Storage(object):
    """Represents the file storage"""

    def __init__(self, path='./'):
        self._path = path

    def collect_file_paths(self):
        """Collect the file paths from the storage directory recursively."""
        return None
