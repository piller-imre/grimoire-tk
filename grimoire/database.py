"""
Simple in-memory database implementation for tagging
"""

from grimoire.context import Context
from grimoire.logger import Logger


class Database(Context):
    """Database for tagging"""

    def __init__(self, path='/tmp/grimoire.log'):
        super(Context, self).__init__()
        self._logger = Logger(path)
        self._context = self._logger.restore_context()
