"""
Repository class definition
"""


class Repository(object):
    """Represents the repository"""

    def __init__(self, database, storage):
        self._database = database
        self._storage = storage

    def collect_untracked_file_paths(self):
        pass

    def collect_missing_file_paths(self):
        pass

    def track_file(self, path):
        pass

    def untrack_document(self, document_id):
        pass
