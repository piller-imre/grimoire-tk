"""
Storage class definition
"""

import os


class Storage(object):
    """Represents the file storage"""

    def __init__(self, path='./'):
        if not os.path.isdir(path):
            os.makedirs(path)
        self._path = path

    def collect_file_paths(self):
        """
        Collect the file paths from the storage directory recursively.
        :return: list of paths as strings
        """
        offset = len(self._path)
        if self._path[-1] != '/':
            offset += 1
        file_paths = []
        for root, dirs, files in os.walk(self._path):
            for name in files:
                file_path = os.path.join(root, name)[offset:]
                file_paths.append(file_path)
        return file_paths
