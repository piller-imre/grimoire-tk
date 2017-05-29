import unittest

from grimoire.context import Context


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
