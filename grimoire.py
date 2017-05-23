"""
Interface for the tagging application
"""

from database import Database


class Grimoire(Database):
    """Tagging application interface"""

    def __init__(self):
        super(Grimoire, self).__init__()
