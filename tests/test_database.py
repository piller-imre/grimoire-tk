import os
import unittest

from grimoire.database import Database

TEST_LOG_PATH = '/tmp/grimoire_test.log'


class DatabaseTest(unittest.TestCase):
    """Unittest for the database"""

    def setUp(self):
        try:
            os.remove(TEST_LOG_PATH)
        except OSError:
            pass

    def test_empty_database(self):
        database = Database(path=TEST_LOG_PATH)
        self.assertEqual(database.count_documents(), 0)
        self.assertEqual(database.count_tags(), 0)
        self.assertEqual(database.count_relations(), 0)

    def test_document_id_creation(self):
        pass

    def test_tag_id_creation(self):
        pass
