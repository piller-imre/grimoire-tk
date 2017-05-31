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
        database = Database(path=TEST_LOG_PATH)
        existing_ids = set()
        for _ in range(1000):
            document_id = database.generate_document_id()
            self.assertNotIn(document_id, existing_ids)
            existing_ids.add(document_id)

    def test_tag_id_creation(self):
        database = Database(path=TEST_LOG_PATH)
        existing_ids = set()
        for _ in range(1000):
            tag_id = database.generate_tag_id()
            self.assertNotIn(tag_id, existing_ids)
            existing_ids.add(tag_id)
