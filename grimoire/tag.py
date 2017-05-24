"""
Tag class definition
"""


class Tag(object):
    """Represents a tag"""

    def __init__(self, id, name):
        if '\n' in name:
            raise ValueError('The tag name cannot contain newline character!')
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
