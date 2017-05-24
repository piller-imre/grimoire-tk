"""
Document class definition
"""


class Document(object):
    """Represents a document"""

    def __init__(self, id, name, type, path):
        if '\n' in name:
            raise ValueError('The document name cannot contain newline character!')
        if '\n' in type:
            raise ValueError('The document type cannot contain newline character!')
        if '\n' in path:
            raise ValueError('The document path cannot contain newline character!')
        self._id = id
        self._name = name
        self._type = type
        self._path = path

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def path(self):
        return self._path
