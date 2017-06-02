import unittest

from grimoire.context import Context


class ContextTest(unittest.TestCase):
    """Unittest for the context class"""

    def test_empty_database(self):
        context = Context()
        self.assertEqual(context.count_documents(), 0)
        self.assertEqual(context.count_tags(), 0)
        self.assertEqual(context.count_relations(), 0)

    def test_document_creation(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        self.assertEqual(context.count_documents(), 1)
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'first.txt')
        self.assertEqual(document.type, 'txt')
        self.assertEqual(document.path, '/tmp/first.txt')

    def test_missing_document(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        with self.assertRaises(ValueError):
            _ = context.get_document(2)

    def test_invalid_document_creation(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        with self.assertRaises(ValueError):
            context.create_document(1, 'second.txt', 'txt', '/tmp/second.txt')

    def test_find_all_documents_from_empty_database(self):
        context = Context()
        documents = context.find_documents([])
        self.assertEqual(documents, [])

    def test_find_all_documents(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.create_document(2, 'second.txt', 'txt', '/tmp/second.txt')
        documents = context.find_documents([])
        self.assertEqual(len(documents), 2)
        self.assertEqual(documents[0].id, 1)
        self.assertEqual(documents[0].name, 'first.txt')
        self.assertEqual(documents[0].type, 'txt')
        self.assertEqual(documents[0].path, '/tmp/first.txt')
        self.assertEqual(documents[1].id, 2)
        self.assertEqual(documents[1].name, 'second.txt')
        self.assertEqual(documents[1].type, 'txt')
        self.assertEqual(documents[1].path, '/tmp/second.txt')

    def test_update_document_name(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.update_document(1, name='second.txt')
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'second.txt')
        self.assertEqual(document.type, 'txt')
        self.assertEqual(document.path, '/tmp/first.txt')

    def test_update_document_type(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.update_document(1, type='csv')
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'first.txt')
        self.assertEqual(document.type, 'csv')
        self.assertEqual(document.path, '/tmp/first.txt')

    def test_update_document_path(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.update_document(1, path='/tmp/here/first.txt')
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'first.txt')
        self.assertEqual(document.type, 'txt')
        self.assertEqual(document.path, '/tmp/here/first.txt')

    def test_update_document(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.update_document(1, 'second.csv', 'csv', '/tmp/second.csv')
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'second.csv')
        self.assertEqual(document.type, 'csv')
        self.assertEqual(document.path, '/tmp/second.csv')

    def test_update_missing_document(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        with self.assertRaises(ValueError):
            context.update_document(2, path='/tmp/nowhere.txt', type='missing')

    def test_remove_document(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.destroy_document(1)
        with self.assertRaises(ValueError):
            _ = context.get_document(1)

    def test_remove_missing_document(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        with self.assertRaises(ValueError):
            context.destroy_document(2)

    def test_reuse_document_identifier(self):
        context = Context()
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        context.destroy_document(1)
        context.create_document(1, 'other.dat', 'data', '/tmp/other.dat')
        document = context.get_document(1)
        self.assertEqual(document.id, 1)
        self.assertEqual(document.name, 'other.dat')
        self.assertEqual(document.type, 'data')
        self.assertEqual(document.path, '/tmp/other.dat')

    def test_document_counting(self):
        context = Context()
        self.assertEqual(context.count_documents(), 0)
        context.create_document(1, 'first.txt', 'txt', '/tmp/first.txt')
        self.assertEqual(context.count_documents(), 1)
        context.create_document(2, 'second.csv', 'csv', '/tmp/second.csv')
        self.assertEqual(context.count_documents(), 2)
        context.create_document(3, 'other.dat', 'data', '/tmp/other.dat')
        self.assertEqual(context.count_documents(), 3)
        context.destroy_document(3)
        self.assertEqual(context.count_documents(), 2)
        context.destroy_document(1)
        self.assertEqual(context.count_documents(), 1)
        context.destroy_document(2)
        self.assertEqual(context.count_documents(), 0)

    def test_tag_creation(self):
        context = Context()
        context.create_tag(1, 'python')
        self.assertEqual(context.count_tags(), 1)
        tag = context.get_tag(1)
        self.assertEqual(tag.id, 1)
        self.assertEqual(tag.name, 'python')

    def test_missing_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        with self.assertRaises(ValueError):
            _ = context.get_tag(2)

    def test_invalid_tag_creation(self):
        context = Context()
        context.create_tag(1, 'python')
        with self.assertRaises(ValueError):
            context.create_tag(1, 'rust')

    def test_find_all_tags_from_empty_database(self):
        context = Context()
        tags = context.find_tags([])
        self.assertEqual(tags, [])

    def test_find_all_tags(self):
        context = Context()
        context.create_tag(1, 'python')
        context.create_tag(2, 'rust')
        tags = context.find_tags([])
        self.assertEqual(len(tags), 2)
        self.assertEqual(tags[0].id, 1)
        self.assertEqual(tags[0].name, 'python')
        self.assertEqual(tags[1].id, 2)
        self.assertEqual(tags[1].name, 'rust')

    def test_update_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        context.update_tag(1, 'lua')
        tag = context.get_tag(1)
        self.assertEqual(tag.id, 1)
        self.assertEqual(tag.name, 'lua')

    def test_update_missing_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        with self.assertRaises(ValueError):
            context.update_tag(2, 'lua')

    def test_remove_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        context.destroy_tag(1)
        with self.assertRaises(ValueError):
            _ = context.get_tag(1)

    def test_remove_missing_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        with self.assertRaises(ValueError):
            context.destroy_tag(2)

    def test_reuse_tag_identifier(self):
        context = Context()
        context.create_tag(1, 'python')
        context.destroy_tag(1)
        context.create_tag(1, 'rust')
        tag = context.get_tag(1)
        self.assertEqual(tag.id, 1)
        self.assertEqual(tag.name, 'rust')

    def test_tag_counting(self):
        context = Context()
        self.assertEqual(context.count_tags(), 0)
        context.create_tag(2, 'rust')
        self.assertEqual(context.count_tags(), 1)
        context.create_tag(1, 'python')
        self.assertEqual(context.count_tags(), 2)
        context.create_tag(3, 'lua')
        self.assertEqual(context.count_tags(), 3)
        context.destroy_tag(2)
        self.assertEqual(context.count_tags(), 2)
        context.destroy_tag(3)
        self.assertEqual(context.count_tags(), 1)
        context.destroy_tag(1)
        self.assertEqual(context.count_tags(), 0)

    def test_unique_tag_name_on_creation(self):
        context = Context()
        context.create_tag(1, 'python')
        with self.assertRaises(ValueError):
            context.create_tag(2, 'python')

    def test_unique_tag_name_on_update(self):
        context = Context()
        context.create_tag(1, 'python')
        context.create_tag(2, 'rust')
        with self.assertRaises(ValueError):
            context.update_tag(2, 'python')

    def test_find_tag_id(self):
        context = Context()
        context.create_tag(1, 'python')
        context.create_tag(2, 'rust')
        context.create_tag(3, 'lua')
        self.assertEqual(context.find_tag_id('rust'), 2)
        self.assertEqual(context.find_tag_id('lua'), 3)
        self.assertEqual(context.find_tag_id('python'), 1)

    def test_find_id_of_missing_tag(self):
        context = Context()
        context.create_tag(1, 'python')
        context.create_tag(2, 'rust')
        context.create_tag(3, 'lua')
        with self.assertRaises(ValueError):
            _ = context.find_tag_id('java')

    def test_create_relations(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'rust.pdf', 'pdf', '/tmp/rust.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_tag(1, 'book')
        context.create_relation(1, 1)
        context.create_relation(2, 1)
        context.create_relation(3, 1)
        document_ids = context.find_document_ids([1])
        self.assertEqual(document_ids, [1, 2, 3])
        self.assertEqual(context.find_tag_ids([1]), [1])
        self.assertEqual(context.find_tag_ids([2]), [1])
        self.assertEqual(context.find_tag_ids([3]), [1])

    def test_create_relation_with_invalid_document(self):
        context = Context()
        context.create_tag(1, 'book')
        with self.assertRaises(ValueError):
            context.create_relation(1, 1)

    def test_create_relation_with_invalid_tag(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        with self.assertRaises(ValueError):
            context.create_relation(1, 1)

    def test_remove_relations(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'rust.pdf', 'pdf', '/tmp/rust.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_tag(1, 'book')
        context.create_relation(1, 1)
        context.create_relation(2, 1)
        context.create_relation(3, 1)
        self.assertEqual(context.count_relations(), 3)
        context.destroy_relation(2, 1)
        self.assertEqual(context.count_relations(), 2)
        context.destroy_relation(1, 1)
        self.assertEqual(context.count_relations(), 1)
        context.destroy_relation(3, 1)
        self.assertEqual(context.count_relations(), 0)

    def test_remove_missing_relation(self):
        context = Context()
        context.create_tag(1, 'book')
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        with self.assertRaises(ValueError):
            context.destroy_relation(1, 1)

    def test_remove_relations_with_document(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'rust.pdf', 'pdf', '/tmp/rust.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_tag(1, 'book')
        context.create_relation(1, 1)
        context.create_relation(2, 1)
        context.create_relation(3, 1)
        context.destroy_document(1)
        self.assertEqual(context.count_relations(), 2)
        context.destroy_document(3)
        self.assertEqual(context.count_relations(), 1)
        context.destroy_document(2)
        self.assertEqual(context.count_relations(), 0)

    def test_remove_relations_with_tag(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'rust.pdf', 'pdf', '/tmp/rust.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_tag(1, 'book')
        context.create_relation(1, 1)
        context.create_relation(2, 1)
        context.create_relation(3, 1)
        context.destroy_tag(1)
        self.assertEqual(context.count_relations(), 0)

    def test_multiple_tags_and_documents(self):
        context = Context()
        context.create_document(1, 'python.pdf', 'pdf', '/tmp/python.pdf')
        context.create_document(2, 'tkinter.pdf', 'pdf', '/tmp/tkinter.pdf')
        context.create_document(3, 'lua.pdf', 'pdf', '/tmp/lua.pdf')
        context.create_document(4, 'index.py', 'py', '/tmp/index.py')
        context.create_tag(5, 'book')
        context.create_tag(6, 'python')
        context.create_relation(1, 5)
        context.create_relation(2, 5)
        context.create_relation(3, 5)
        context.create_relation(1, 6)
        context.create_relation(2, 6)
        context.create_relation(4, 6)
        self.assertEqual(context.count_relations(), 6)
        book_ids = context.find_document_ids([5])
        self.assertEqual(book_ids, [1, 2, 3])
        python_ids = context.find_document_ids([6])
        self.assertEqual(python_ids, [1, 2, 4])
        python_book_ids = context.find_document_ids([5, 6])
        self.assertEqual(python_book_ids, [1, 2])
        document_ids = context.find_document_ids([])
        self.assertEqual(document_ids, [1, 2, 3, 4])
        tag_ids = context.find_tag_ids([1, 2])
        self.assertEqual(tag_ids, [5, 6])
        tag_ids = context.find_tag_ids([1, 3])
        self.assertEqual(tag_ids, [5])
        tag_ids = context.find_tag_ids([3, 4])
        self.assertEqual(tag_ids, [])
