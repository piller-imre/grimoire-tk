import unittest

from grimoire.context import Context
from grimoire.scope import Scope


class ScopeTest(unittest.TestCase):
    """Unittest for the scope class"""

    def setUp(self):
        """Create a sample context for tests."""
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'rust.pdf', 'pdf', '/tmp/rust.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_document(4, 'index.py', 'python', '/tmp/index.py')
        context.create_document(5, 'tkinter.pdf', 'pdf', '/tmp/tkinter.pdf')
        context.create_document(6, 'gui.lua', 'lua', '/tmp/gui.lua')
        context.create_document(7, 'index.rs', 'rust', '/tmp/index.rs')
        context.create_document(8, 'gui.rs', 'rust', '/tmp/gui.rs')
        context.create_tag(1, 'book')
        context.create_tag(2, 'python')
        context.create_tag(3, 'rust')
        context.create_tag(4, 'lua')
        context.create_tag(5, 'gui')
        context.create_tag(6, 'index')
        relations = [
            (1, 1), (1, 2),
            (2, 1), (2, 3),
            (3, 1), (3, 4),
            (4, 2), (4, 6),
            (5, 1), (5, 2), (5, 5),
            (6, 4), (6, 5),
            (7, 3), (7, 6),
            (8, 3), (8, 5)
        ]
        for relation in relations:
            context.create_relation(relation[0], relation[1])
        self._context = context

    def test_initial_scope(self):
        pass

    def test_document_creation_without_tags(self):
        pass

    def test_document_creation_with_single_tag(self):
        pass

    def test_document_creation_with_multiple_tags(self):
        pass

    def test_document_copy_to_root(self):
        pass

    def test_document_copy_with_single_tag(self):
        pass

    def test_document_copy_with_multiple_tags(self):
        pass

    def test_invalid_document_copy(self):
        pass

    def test_single_document_move_to_root(self):
        pass

    def test_multiple_document_move_to_root(self):
        pass

    def test_document_move_with_single_tag(self):
        pass

    def test_document_move_with_multiple_tags(self):
        pass

    def test_invalid_document_move(self):
        pass

    def test_document_destroying(self):
        pass

    def test_invalid_document_destroying(self):
        pass

    def test_get_document(self):
        pass

    def test_get_invalid_document(self):
        pass

    def test_get_documents_of_root(self):
        pass

    def test_get_documents_with_single_tag(self):
        pass

    def test_get_documents_with_multiple_tags(self):
        pass

    def test_toggle_document_selection(self):
        pass

    def test_invalid_toggle_document_selection(self):
        pass

    def test_document_selection(self):
        pass

    def test_invalid_document_selection(self):
        pass

    def test_document_deselection(self):
        pass

    def test_invalid_document_deselection(self):
        pass

    def test_deselect_all_documents(self):
        pass

    def test_tag_creation_without_documents(self):
        pass

    def test_tag_creation_with_single_document(self):
        pass

    def test_tag_creation_with_multiple_documents(self):
        pass

    def test_duplicated_tag_creation(self):
        pass

    def test_tag_addition_without_selection(self):
        pass

    def test_tag_addition_with_single_selection(self):
        pass

    def test_tag_addition_with_multiple_selection(self):
        pass

    def test_invalid_tag_addition(self):
        pass

    def test_tag_removing_without_selection(self):
        pass

    def test_tag_removing_with_selection_from_query(self):
        pass

    def test_tag_removing_with_selection_from_document(self):
        pass

    def test_invalid_tag_removing(self):
        pass

    def test_tag_destroying(self):
        pass

    def test_get_scope_tags_without_selection(self):
        pass

    def test_get_scope_tags_with_selection(self):
        pass

    def test_get_document_only_tags_without_selection(self):
        pass

    def test_get_document_only_tags_with_selection(self):
        pass
