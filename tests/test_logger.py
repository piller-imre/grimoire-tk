import os
import unittest

from grimoire.context import Context
from grimoire.logger import Logger

TEST_LOG_PATH = '/tmp/grimoire_test.log'


class LoggerTest(unittest.TestCase):
    """Unittest for the logger"""

    def setUp(self):
        try:
            os.remove(TEST_LOG_PATH)
        except OSError:
            pass

    def test_empty_context(self):
        logger = Logger(path=TEST_LOG_PATH)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 0)
        self.assertEqual(context.count_tags(), 0)
        self.assertEqual(context.count_relations(), 0)

    def test_document_creation(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 1,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 1)
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'first.txt')
        self.assertEqual(document.type, 'txt')
        self.assertEqual(document.path, '/tmp/first.txt')

    def test_document_creation_and_remove(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 1,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'destroy_document',
            'id': 1
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 0)

    def test_tag_creation(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_tag',
            'id': 123,
            'name': 'python'
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_tags(), 1)
        tag = context.get_tag(123)
        self.assertEqual(tag.id, 123)
        self.assertEqual(tag.name, 'python')

    def test_tag_creation_and_remove(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_tag',
            'id': 123,
            'name': 'python'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'destroy_tag',
            'id': 123
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_tags(), 0)

    def test_relation_creation(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 456,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'create_tag',
            'id': 123,
            'name': 'python'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'create_relation',
            'document_id': 456,
            'tag_id': 123
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 1)
        self.assertEqual(context.count_tags(), 1)
        self.assertEqual(context.count_relations(), 1)
        self.assertEqual(context.find_document_ids([123]), [456])
        self.assertEqual(context.find_tag_ids([456]), [123])

    def test_relation_creation_and_remove(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 456,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'create_tag',
            'id': 123,
            'name': 'python'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'create_relation',
            'document_id': 456,
            'tag_id': 123
        }
        logger.save_operation(operation)
        operation = {
            'method': 'destroy_relation',
            'document_id': 456,
            'tag_id': 123
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 1)
        self.assertEqual(context.count_tags(), 1)
        self.assertEqual(context.count_relations(), 0)
        self.assertEqual(context.find_document_ids([123]), [])
        self.assertEqual(context.find_document_ids([]), [456])
        self.assertEqual(context.find_tag_ids([456]), [])
        self.assertEqual(context.find_tag_ids([]), [123])

    def test_document_name_update(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 456,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'update_document',
            'id': 456,
            'name': 'new.rst'
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 1)
        document = context.get_document(456)
        self.assertEqual(document.id, 456)
        self.assertEqual(document.name, 'new.rst')
        self.assertEqual(document.type, 'txt')
        self.assertEqual(document.path, '/tmp/first.txt')

    def test_document_path_and_type_update(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_document',
            'id': 456,
            'name': 'first.txt',
            'type': 'txt',
            'path': '/tmp/first.txt'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'update_document',
            'id': 456,
            'path': '/tmp/new.rst',
            'type': 'rst'
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_documents(), 1)
        document = context.get_document(456)
        self.assertEqual(document.id, 456)
        self.assertEqual(document.name, 'first.txt')
        self.assertEqual(document.type, 'rst')
        self.assertEqual(document.path, '/tmp/new.rst')

    def test_tag_name_update(self):
        logger = Logger(path=TEST_LOG_PATH)
        operation = {
            'method': 'create_tag',
            'id': 123,
            'name': 'python'
        }
        logger.save_operation(operation)
        operation = {
            'method': 'update_tag',
            'id': 123,
            'name': 'lua'
        }
        logger.save_operation(operation)
        context = Context()
        logger.restore_context(context)
        self.assertEqual(context.count_tags(), 1)
        tag = context.get_tag(123)
        self.assertEqual(tag.id, 123)
        self.assertEqual(tag.name, 'lua')
