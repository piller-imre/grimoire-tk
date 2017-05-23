"""
Interface for the tagging application
"""

from database import Database
from logger import Logger


class Grimoire(Database):
    """Tagging application interface"""

    def __init__(self):
        super(Grimoire, self).__init__()
        self._logger = Logger('/tmp/grimoire.log')
        self._logger.restore_database(self)

