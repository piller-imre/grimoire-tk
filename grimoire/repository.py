"""
Repository class definition
"""

import os


class Repository(object):
    """Represents the repository"""

    def __init__(self, database, storage):
        self._database = database
        self._storage = storage

    def collect_untracked_file_paths(self):
        """
        Collect file paths in the storage which are not tracked in the database.
        :return: list of file paths
        """
        document_paths = self._database.collect_document_paths()
        file_paths = self._storage.collect_file_paths()
        return set(file_paths) - document_paths

    def collect_missing_file_paths(self):
        """
        Collect file paths which are in the database but not in the storage.
        :return: list of file paths
        """
        document_paths = self._database.collect_document_paths()
        file_paths = self._storage.collect_file_paths()
        return document_paths - set(file_paths)

    def track_file(self, path):
        """
        Track the given file in the database.
        :param path:
        :return:
        """
        absolute_path = os.path.join(self._storage.path, path)
        if not os.path.isfile(absolute_path):
            raise ValueError('Invalid file path! {}'.format(absolute_path))
        name = os.path.basename(path)
        extension = os.path.splitext(path)[1]
        document_type = ''
        if len(extension) > 1:
            document_type = extension[1:]
        document = self._database.create_document(name=name, type=document_type, path=path)
        return document.id

    def untrack_document(self, document_id):
        """
        Do not track the given document in the database.
        :param document_id: the identifier of the document as an integer value
        :return: None
        """
        _ = self._database.get_document(document_id)
        self._database.destroy_document(id=document_id)
