import os
import unittest

from grimoire.database import Database
from grimoire.scope import Scope

TEST_LOG_PATH = '/tmp/grimoire_test.log'

sample_documents = {
    1: {'name': 'python.pdf', 'type': 'pdf', 'path': '/tmp/python.pdf'},
    2: {'name': 'rust.pdf', 'type': 'pdf', 'path': '/tmp/rust.pdf'},
    3: {'name': 'lua.pdf', 'type': 'pdf', 'path': '/tmp/lua.pdf'},
    4: {'name': 'index.py', 'type': 'python', 'path': '/tmp/index.py'},
    5: {'name': 'tkinter.pdf', 'type': 'pdf', 'path': '/tmp/tkinter.pdf'},
    6: {'name': 'gui.lua', 'type': 'lua', 'path': '/tmp/gui.lua'},
    7: {'name': 'index.rs', 'type': 'rust', 'path': '/tmp/index.rs'},
    8: {'name': 'gui.rs', 'type': 'rust', 'path': '/tmp/gui.rs'}
}

sample_tags = {
    1: 'book',
    2: 'python',
    3: 'rust',
    4: 'lua',
    5: 'gui',
    6: 'index'
}

sample_relations = [
    (1, 1), (1, 2),
    (2, 1), (2, 3),
    (3, 1), (3, 4),
    (4, 2), (4, 6),
    (5, 1), (5, 2), (5, 5),
    (6, 4), (6, 5),
    (7, 3), (7, 6),
    (8, 3), (8, 5)
]


def create_sample_database():
    """
    Create a sample database for testing.
    :return: a `Context` object
    """
    database = Database(path=TEST_LOG_PATH)
    for document_id in range(1, 9):
        database.create_document(**sample_documents[document_id])
    for tag_id in range(1, 7):
        database.create_tag(name=sample_tags[tag_id])
    for relation in sample_relations:
        database.create_relation(document_id=relation[0], tag_id=relation[1])
    return database


class ScopeTest(unittest.TestCase):
    """Unittest for the scope class"""

    def setUp(self):
        """Initialize a sample context for tests."""
        try:
            os.remove(TEST_LOG_PATH)
        except OSError:
            pass
        self._database = create_sample_database()

    def test_initial_scope(self):
        scope = Scope(database=self._database)
        concept_document_ids = scope.get_concept_document_ids()
        self.assertEqual(set(concept_document_ids), {1, 2, 3, 4, 5, 6, 7, 8})
        concept_documents = scope.get_concept_documents()
        for concept_document in concept_documents:
            self.assertIn(concept_document.id, sample_documents)
            self.assertEqual(concept_document.name, sample_documents[concept_document.id]['name'])
            self.assertEqual(concept_document.type, sample_documents[concept_document.id]['type'])
            self.assertEqual(concept_document.path, sample_documents[concept_document.id]['path'])
        concept_tag_ids = scope.get_concept_tag_ids()
        self.assertEqual(concept_tag_ids, [])
        concept_tags = scope.get_concept_tags()
        self.assertEqual(concept_tags, [])
        selection_document_ids = scope.get_selection_document_ids()
        self.assertEqual(selection_document_ids, [])
        selection_documents = scope.get_selection_documents()
        self.assertEqual(selection_documents, [])
        selection_tag_ids = scope.get_selection_tag_ids()
        self.assertEqual(set(selection_tag_ids), {1, 2, 3, 4, 5, 6})
        selection_tags = scope.get_selection_tags()
        for selection_tag in selection_tags:
            self.assertIn(selection_tag.id, sample_tags)
            self.assertEqual(selection_tag.name, sample_tags[selection_tag.id])
        concept_only_document_ids = scope.get_concept_only_document_ids()
        self.assertEqual(set(concept_only_document_ids), set(concept_document_ids))
        concept_only_documents = scope.get_concept_only_documents()
        for concept_only_document in concept_only_documents:
            self.assertIn(concept_only_document.id, sample_documents)
            self.assertEqual(concept_only_document.name, sample_documents[concept_only_document.id]['name'])
            self.assertEqual(concept_only_document.type, sample_documents[concept_only_document.id]['type'])
            self.assertEqual(concept_only_document.path, sample_documents[concept_only_document.id]['path'])
        selection_only_tag_ids = scope.get_selection_only_tag_ids()
        self.assertEqual(set(selection_only_tag_ids), {1, 2, 3, 4, 5, 6})
        selection_only_tags = scope.get_selection_only_tags()
        for selection_only_tag in selection_only_tags:
            self.assertIn(selection_only_tag.id, sample_tags)
            self.assertEqual(selection_only_tag.name, sample_tags[selection_only_tag.id])

    def test_document_creation_without_tags(self):
        scope = Scope(database=self._database)
        document = scope.create_document('main.c', 'c', '/tmp/main.c')
        scope.select_document(document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [document.id])
        self.assertEqual(scope.get_selection_tag_ids(), [])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_document_creation_with_single_tag(self):
        scope = Scope(database=self._database)
        scope.add_tag(2)
        self.assertEqual(scope.get_concept_tag_ids(), [2])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 3, 4, 5, 6})
        document = scope.create_document('main.py', 'python', '/tmp/main.py')
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 4, 5, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [2])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 4, 5, document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 3, 4, 5, 6})
        scope.select_document(document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 4, 5, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [2])
        self.assertEqual(scope.get_selection_document_ids(), [document.id])
        self.assertEqual(scope.get_selection_tag_ids(), [2])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 4, 5})
        self.assertEqual(scope.get_selection_only_tag_ids(), [])
        scope.deselect_document(document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 4, 5, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [2])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 4, 5, document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 3, 4, 5, 6})
        scope.remove_tag(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [document.id])
        self.assertEqual(scope.get_selection_tag_ids(), [2])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [2])

    def test_document_creation_with_multiple_tags(self):
        scope = Scope(database=self._database)
        scope.add_tag(4)
        self.assertEqual(set(scope.get_concept_document_ids()), {3, 6})
        self.assertEqual(scope.get_concept_tag_ids(), [4])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 5, 6})
        scope.add_tag(1)
        self.assertEqual(scope.get_concept_document_ids(), [3])
        self.assertEqual(set(scope.get_concept_tag_ids()), {1, 4})
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {2, 3, 5, 6})
        scope.add_tag(2)
        self.assertEqual(scope.get_concept_document_ids(), [])
        self.assertEqual(set(scope.get_concept_tag_ids()), {1, 2, 4})
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {3, 5, 6})
        document = scope.create_document('vm.pdf', 'pdf', '/tmp/vm.pdf')
        self.assertEqual(scope.get_concept_document_ids(), [document.id])
        self.assertEqual(set(scope.get_concept_tag_ids()), {1, 2, 4})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [document.id])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {3, 5, 6})
        scope.select_document(document.id)
        self.assertEqual(scope.get_concept_document_ids(), [document.id])
        self.assertEqual(set(scope.get_concept_tag_ids()), {1, 2, 4})
        self.assertEqual(scope.get_selection_document_ids(), [document.id])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 4})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_document_copy_to_root(self):
        scope = Scope(database=self._database)
        scope.copy_document(7)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(7)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(set(scope.get_selection_tag_ids()), {3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {3, 6})
        scope.add_tag(3)
        self.assertEqual(set(scope.get_concept_document_ids()), {2, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [3])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(set(scope.get_selection_tag_ids()), {3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {2, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [6])
        scope.remove_tag(3)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(set(scope.get_selection_tag_ids()), {3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {3, 6})
        scope.add_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(set(scope.get_selection_tag_ids()), {3, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [4])
        self.assertEqual(scope.get_selection_only_tag_ids(), [3])
        scope.remove_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(set(scope.get_selection_tag_ids()), {3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {3, 6})

    def test_document_copy_with_single_tag(self):
        scope = Scope(database=self._database)
        scope.add_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        scope.copy_document(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {2, 4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {2, 4, 7})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        scope.remove_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [2])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 3, 6})

    def test_document_copy_with_multiple_tags(self):
        scope = Scope(database=self._database)
        scope.add_tag(2)
        scope.add_tag(3)
        scope.add_tag(6)
        self.assertEqual(scope.get_concept_document_ids(), [])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        scope.copy_document(6)
        self.assertEqual(scope.get_concept_document_ids(), [6])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [6])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        scope.select_document(6)
        self.assertEqual(scope.get_concept_document_ids(), [6])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [6])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {4, 5})

    def test_invalid_document_copy(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.copy_document(9)

    def test_single_document_move_to_root(self):
        scope = Scope(database=self._database)
        scope.move_document(7)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(7)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [7])
        self.assertEqual(scope.get_selection_tag_ids(), [])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_document_move_with_single_tag(self):
        scope = Scope(database=self._database)
        scope.add_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        scope.move_document(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {2, 4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {2, 4, 7})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        scope.remove_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [2])
        self.assertEqual(scope.get_selection_tag_ids(), [6])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [6])

    def test_document_move_with_multiple_tags(self):
        scope = Scope(database=self._database)
        scope.add_tag(2)
        scope.add_tag(3)
        scope.add_tag(6)
        self.assertEqual(scope.get_concept_document_ids(), [])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        scope.move_document(6)
        self.assertEqual(scope.get_concept_document_ids(), [6])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [6])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        scope.select_document(6)
        self.assertEqual(scope.get_concept_document_ids(), [6])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [6])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_invalid_document_move(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.move_document(9)

    def test_document_clone_to_root(self):
        scope = Scope(database=self._database)
        cloned_document = scope.clone_document(7)
        self.assertNotEqual(cloned_document.id, 7)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(cloned_document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(scope.get_selection_tag_ids(), [])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_document_clone_with_single_tag(self):
        scope = Scope(database=self._database)
        scope.add_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        cloned_document = scope.clone_document(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [6])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {4, 7, cloned_document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5})
        scope.remove_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        scope.select_document(cloned_document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(scope.get_selection_tag_ids(), [6])
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(scope.get_selection_only_tag_ids(), [6])

    def test_document_clone_with_multiple_tags(self):
        scope = Scope(database=self._database)
        scope.add_tag(2)
        scope.add_tag(3)
        scope.add_tag(6)
        self.assertEqual(scope.get_concept_document_ids(), [])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        cloned_document = scope.clone_document(6)
        self.assertNotEqual(cloned_document.id, 6)
        self.assertEqual(scope.get_concept_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 4, 5})
        scope.select_document(cloned_document.id)
        self.assertEqual(scope.get_concept_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(scope.get_selection_only_tag_ids(), [])
        scope.remove_tag(3)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, cloned_document.id})
        self.assertEqual(set(scope.get_concept_tag_ids()), {2, 6})
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 6})
        self.assertEqual(scope.get_concept_only_document_ids(), [4])
        self.assertEqual(scope.get_selection_only_tag_ids(), [3])
        scope.remove_tag(2)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 7, cloned_document.id})
        self.assertEqual(set(scope.get_concept_tag_ids()), {6})
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {4, 7})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {2, 3})
        scope.remove_tag(6)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [cloned_document.id])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 3, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {2, 3, 6})
        scope.deselect_document(cloned_document.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(scope.get_concept_tag_ids(), [])
        self.assertEqual(scope.get_selection_document_ids(), [])
        self.assertEqual(set(scope.get_selection_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(set(scope.get_concept_only_document_ids()), {1, 2, 3, 4, 5, 6, 7, 8, cloned_document.id})
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        document_counts = {
            1: 4,
            2: 3 + 1,
            3: 3 + 1,
            4: 2,
            5: 3,
            6: 2 + 1
        }
        for tag_id, document_count in document_counts.items():
            scope.add_tag(tag_id)
            self.assertEqual(len(scope.get_concept_documents()), document_count)
            scope.remove_tag(tag_id)

    def test_invalid_document_clone(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            _ = scope.clone_document(9)

    def test_document_destroying(self):
        scope = Scope(database=self._database)
        document_counts = {
            1: [4, 3, 2, 1, 1, 0, 0, 0, 0],
            2: [3, 2, 2, 2, 1, 0, 0, 0, 0],
            3: [3, 3, 2, 2, 2, 2, 2, 1, 0],
            4: [2, 2, 2, 1, 1, 1, 0, 0, 0],
            5: [3, 3, 3, 3, 3, 2, 1, 1, 0],
            6: [2, 2, 2, 2, 1, 1, 1, 0, 0]
        }
        for i in range(9):
            if i > 0:
                scope.destroy_document(i)
            for tag_id in range(1, 7):
                scope.add_tag(tag_id)
                self.assertEqual(len(scope.get_concept_documents()), document_counts[tag_id][i])
                scope.remove_tag(tag_id)

    def test_invalid_document_destroying(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.destroy_document(9)

    def test_duplicated_document_destroying(self):
        scope = Scope(database=self._database)
        for document_id in range(1, 9):
            scope.destroy_document(document_id)
            with self.assertRaises(ValueError):
                scope.destroy_document(document_id)

    def test_get_document(self):
        scope = Scope(database=self._database)
        for document_id in range(1, 9):
            document = scope.get_document(document_id)
            self.assertEqual(document.id, document_id)
            self.assertEqual(document.name, sample_documents[document_id]['name'])
            self.assertEqual(document.type, sample_documents[document_id]['type'])
            self.assertEqual(document.path, sample_documents[document_id]['path'])

    def test_get_invalid_document(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            _ = scope.get_document(0)
        with self.assertRaises(ValueError):
            _ = scope.get_document(9)

    def test_get_documents_with_single_tag(self):
        scope = Scope(database=self._database)
        document_ids = {
            1: [1, 2, 3, 5],
            2: [1, 4, 5],
            3: [2, 7, 8],
            4: [3, 6],
            5: [5, 6, 8],
            6: [4, 7]
        }
        for tag_id, document_ids in document_ids.items():
            self.assertEqual(scope.get_concept_tags(), [])
            scope.add_tag(tag_id)
            documents = scope.get_concept_documents()
            self.assertEqual(len(documents), len(document_ids))
            for document in documents:
                self.assertIn(document.id, document_ids)
            scope.remove_tag(tag_id)
            self.assertEqual(scope.get_concept_tags(), [])

    def test_get_documents_with_multiple_tags(self):
        scope = Scope(database=self._database)
        tag_selections = {
            (1, 2): [1, 5],
            (1, 3): [2],
            (1, 4): [3],
            (1, 5): [5],
            (1, 6): [],
            (2, 5): [5],
            (3, 6): [7],
            (1, 2, 5): [5],
            (3, 5, 6): [],
            (1, 2, 3, 4, 5, 6): []
        }
        for selection, document_ids in tag_selections.items():
            self.assertEqual(scope.get_concept_tags(), [])
            for tag_id in selection:
                scope.add_tag(tag_id)
            documents = scope.get_concept_documents()
            self.assertEqual(len(documents), len(document_ids))
            for document in documents:
                self.assertIn(document.id, document_ids)
            for tag_id in selection:
                scope.remove_tag(tag_id)
            self.assertEqual(scope.get_concept_tags(), [])

    def test_toggle_document_selection(self):
        scope = Scope(database=self._database)
        toggle_items = [
            {'document_id': 1, 'tag_ids': [1, 2]},
            {'document_id': 2, 'tag_ids': [1]},
            {'document_id': 1, 'tag_ids': [1, 3]},
            {'document_id': 7, 'tag_ids': [3]},
            {'document_id': 8, 'tag_ids': [3]},
            {'document_id': 6, 'tag_ids': []},
            {'document_id': 2, 'tag_ids': []},
            {'document_id': 7, 'tag_ids': [5]},
            {'document_id': 8, 'tag_ids': [4, 5]}
        ]
        for item in toggle_items:
            scope.toggle_document_selection(item['document_id'])
            selection_only_tags = scope.get_selection_only_tags()
            self.assertEqual(len(selection_only_tags), len(item['tag_ids']))
            for tag in selection_only_tags:
                self.assertIn(tag.id, item['tag_ids'])

    def test_invalid_toggle_document_selection(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            _ = scope.toggle_document_selection(0)
        with self.assertRaises(ValueError):
            _ = scope.toggle_document_selection(9)

    def test_document_selection(self):
        scope = Scope(database=self._database)
        document_selections = {
            (1, 2): [1],
            (1, 5): [1, 2],
            (2, 7): [3],
            (5, 6, 8): [5],
            (2, 7, 8): [3],
            (3, 4): [],
            (5, 7): [],
            (1, 2, 3, 4, 5, 6, 7, 8): []
        }
        for selection, tag_ids in document_selections.items():
            for document_id in selection:
                scope.select_document(document_id)
            selection_only_tags = scope.get_selection_only_tags()
            self.assertEqual(len(selection_only_tags), len(tag_ids))
            for tag in selection_only_tags:
                self.assertIn(tag.id, tag_ids)
            for document_id in selection:
                scope.deselect_document(document_id)

    def test_invalid_document_selection(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            _ = scope.select_document(0)
        with self.assertRaises(ValueError):
            _ = scope.select_document(9)

    def test_document_deselection(self):
        scope = Scope(database=self._database)
        expected_tag_ids = {
            6: [2],
            4: [1, 2],
            1: [1, 2, 5]
        }
        for document_id in [1, 4, 5, 6]:
            scope.select_document(document_id)
        for document_id in [6, 4, 1]:
            scope.deselect_document(document_id)
            selection_only_tags = scope.get_selection_only_tags()
            self.assertEqual(len(selection_only_tags), len(expected_tag_ids[document_id]))
            for tag in selection_only_tags:
                self.assertIn(tag.id, expected_tag_ids[document_id])

    def test_invalid_document_deselection(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            _ = scope.deselect_document(0)
        with self.assertRaises(ValueError):
            _ = scope.deselect_document(9)

    def test_deselect_all_documents(self):
        scope = Scope(database=self._database)
        for last_document_id in range(1, 10):
            for document_id in range(1, last_document_id):
                scope.select_document(document_id)
            self.assertEqual(len(scope.get_selection_documents()), last_document_id - 1)
            scope.deselect_all_documents()
            self.assertEqual(scope.get_selection_documents(), [])

    def test_tag_creation_without_document(self):
        scope = Scope(database=self._database)
        self.assertEqual(scope.get_concept_tags(), [])
        tag = scope.create_tag('n+1')
        scope.add_tag(tag.id)
        self.assertEqual(scope.get_concept_tag_ids(), [tag.id])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {1, 2, 3, 4, 5, 6})
        self.assertEqual(scope.get_concept_documents(), [])

    def test_tag_creation_with_single_document(self):
        scope = Scope(database=self._database)
        scope.select_document(4)
        tag = scope.create_tag('template')
        scope.add_tag(tag.id)
        self.assertEqual(scope.get_concept_document_ids(), [4])
        self.assertEqual(scope.get_concept_tag_ids(), [tag.id])
        self.assertEqual(scope.get_selection_document_ids(), [4])
        self.assertEqual(set(scope.get_selection_tag_ids()), {2, 6, tag.id})
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(set(scope.get_selection_only_tag_ids()), {2, 6})
        tag_names = {
            2: 'python',
            6: 'index',
            tag.id: 'template'
        }
        for tag in scope.get_selection_only_tags():
            self.assertEqual(tag.name, tag_names[tag.id])

    def test_tag_creation_with_multiple_documents(self):
        scope = Scope(database=self._database)
        for document_id in [4, 6, 7, 8]:
            scope.select_document(document_id)
        tag = scope.create_tag('source')
        scope.add_tag(tag.id)
        self.assertEqual(set(scope.get_concept_document_ids()), {4, 6, 7, 8})
        self.assertEqual(scope.get_concept_tag_ids(), [tag.id])
        self.assertEqual(set(scope.get_selection_document_ids()), {4, 6, 7, 8})
        self.assertEqual(scope.get_selection_tag_ids(), [tag.id])
        self.assertEqual(scope.get_concept_only_document_ids(), [])
        self.assertEqual(scope.get_selection_only_tag_ids(), [])

    def test_duplicated_tag_creation(self):
        scope = Scope(database=self._database)
        _ = scope.create_tag('unique')
        with self.assertRaises(ValueError):
            _ = scope.create_tag('unique')

    def test_tag_addition_without_selection(self):
        scope = Scope(database=self._database)
        self.assertEqual(len(scope.get_concept_tags()), 0)
        for tag_id in range(1, 7):
            scope.add_tag(tag_id)
            self.assertEqual(len(scope.get_concept_tags()), tag_id)

    def test_tag_addition_with_single_selection(self):
        scope = Scope(database=self._database)
        scope.select_document(7)
        self.assertEqual(scope.get_concept_tags(), [])
        document_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(document_only_tags), 2)
        _ = scope.create_tag('script')
        _ = scope.create_tag('web')
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 4)
        for tag in selection_only_tags:
            self.assertIn(tag.name, ['rust', 'index', 'script', 'web'])

    def test_tag_addition_with_multiple_selection(self):
        scope = Scope(database=self._database)
        scope.select_document(7)
        scope.select_document(8)
        self.assertEqual(scope.get_concept_tags(), [])
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 1)
        _ = scope.create_tag('script')
        _ = scope.create_tag('web')
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 3)
        for tag in selection_only_tags:
            self.assertIn(tag.name, ['rust', 'script', 'web'])

    def test_invalid_tag_addition(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.add_tag(0)
        with self.assertRaises(ValueError):
            scope.add_tag(11)

    def test_tag_removing_without_selection(self):
        scope = Scope(database=self._database)
        self.assertEqual(len(scope.get_concept_tags()), 0)
        for tag_id in range(1, 7):
            scope.add_tag(tag_id)
        self.assertEqual(len(scope.get_concept_tags()), 6)
        for tag_id in range(1, 7):
            scope.remove_tag(tag_id)
            self.assertEqual(len(scope.get_concept_tags()), 6 - tag_id)

    def test_tag_removing_with_selection_from_query(self):
        scope = Scope(database=self._database)
        scope.add_tag(5)
        scope.add_tag(1)
        scope.select_document(5)
        concept_tags = scope.get_concept_tags()
        self.assertEqual(len(concept_tags), 2)
        for tag in concept_tags:
            self.assertIn(tag.name, ['book', 'gui'])
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 1)
        self.assertEqual(selection_only_tags[0].name, 'python')
        scope.remove_tag(5)
        concept_tags = scope.get_concept_tags()
        self.assertEqual(len(concept_tags), 1)
        self.assertEqual(concept_tags[0].name, 'book')
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 2)
        for tag in selection_only_tags:
            self.assertIn(tag.name, ['gui', 'python'])

    def test_tag_removing_with_selection_from_document(self):
        scope = Scope(database=self._database)
        scope.add_tag(2)
        scope.add_tag(5)
        scope.select_document(5)
        concept_tags = scope.get_concept_tags()
        self.assertEqual(len(concept_tags), 2)
        for tag in concept_tags:
            self.assertIn(tag.name, ['gui', 'python'])
        selection_only_tags = scope.get_selection_only_tags()
        self.assertEqual(len(selection_only_tags), 1)
        self.assertEqual(selection_only_tags[0].name, 'book')
        scope.remove_tag(1)
        concept_tags = scope.get_concept_tags()
        self.assertEqual(len(concept_tags), 2)
        for tag in concept_tags:
            self.assertIn(tag.name, ['gui', 'python'])
        self.assertEqual(scope.get_selection_only_tags(), [])

    def test_invalid_tag_removing(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.remove_tag(11)
        with self.assertRaises(ValueError):
            scope.remove_tag(0)

    def test_tag_destroying(self):
        scope = Scope(database=self._database)
        tag_counts = {
            1: [2, 1, 0, 0, 0, 0, 0],
            2: [2, 1, 1, 0, 0, 0, 0],
            3: [2, 1, 1, 1, 0, 0, 0],
            4: [2, 2, 1, 1, 1, 1, 0],
            5: [3, 2, 1, 1, 1, 0, 0],
            6: [2, 2, 2, 2, 1, 0, 0],
            7: [2, 2, 2, 1, 1, 1, 0],
            8: [2, 2, 2, 1, 1, 0, 0]
        }
        for i in range(7):
            if i > 0:
                scope.destroy_tag(i)
            for document_id in range(1, 9):
                scope.select_document(document_id)
                self.assertEqual(len(scope.get_selection_only_tags()), tag_counts[document_id][i])
                scope.deselect_document(document_id)

    def test_invalid_tag_destroying(self):
        scope = Scope(database=self._database)
        with self.assertRaises(ValueError):
            scope.destroy_tag(0)
        with self.assertRaises(ValueError):
            scope.destroy_tag(11)

    def test_duplicated_tag_destroying(self):
        scope = Scope(database=self._database)
        for tag_id in range(1, 7):
            scope.destroy_tag(tag_id)
            with self.assertRaises(ValueError):
                scope.destroy_tag(tag_id)
