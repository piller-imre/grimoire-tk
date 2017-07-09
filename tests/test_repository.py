import os
import shutil
import unittest

from grimoire.repository import Repository
from grimoire.database import Database
from grimoire.storage import Storage

TEST_LOG_PATH = '/tmp/grimoire_test.log'
TEST_ROOT_PATH = '/tmp/grimoire_test_storage/'


def touch(path, times=None):
    """A Python implementation of the touch command."""
    with open(path, 'a'):
        os.utime(path, times)


class RepositoryTest(unittest.TestCase):
    """Unittest for the repository"""

    def setUp(self):
        """Remove the storage directory if exists."""
        try:
            os.remove(TEST_LOG_PATH)
        except OSError:
            pass
        try:
            shutil.rmtree(TEST_ROOT_PATH)
        except FileNotFoundError:
            pass

    def test_empty_database_and_storage(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        repository = Repository(database, storage)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(len(untracked_files), 0)
        missing_files = repository.collect_missing_file_paths()
        self.assertEqual(len(missing_files), 0)

    def test_untracked_files(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        paths = {'first.txt', 'second.txt', 'third.txt'}
        for path in paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        untracked_file_paths = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_file_paths, paths)

    def test_missing_files(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        documents = [
            {
                'name': 'first.txt',
                'type': 'txt',
                'path': 'first.txt'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'images/second.png'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'second.png'
            }
        ]
        paths = {
            'first.txt', 'second.png', 'images/second.png'
        }
        for document in documents:
            database.create_document(**document)
        repository = Repository(database, storage)
        missing_file_paths = repository.collect_missing_file_paths()
        self.assertEqual(missing_file_paths, paths)

    def test_missing_and_untracked_files(self):
        database = Database(TEST_LOG_PATH)
        documents = [
            {
                'name': 'first.txt',
                'type': 'txt',
                'path': 'first.txt'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'images/second.png'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'second.png'
            }
        ]
        for document in documents:
            database.create_document(**document)
        storage = Storage(TEST_ROOT_PATH)
        storage_paths = {'first.txt', 'second.txt', 'third.txt'}
        for path in storage_paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'second.txt', 'third.txt'})
        missing_files = repository.collect_missing_file_paths()
        self.assertEqual(missing_files, {'second.png', 'images/second.png'})

    def test_matching_database_and_storage(self):
        database = Database(TEST_LOG_PATH)
        documents = [
            {
                'name': 'first.txt',
                'type': 'txt',
                'path': 'first.txt'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'images/second.png'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'second.png'
            }
        ]
        for document in documents:
            database.create_document(**document)
        storage = Storage(TEST_ROOT_PATH)
        storage_paths = {'first.txt', 'images/second.png', 'second.png'}
        os.mkdir(TEST_ROOT_PATH + 'images')
        for path in storage_paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(len(untracked_files), 0)
        missing_files = repository.collect_missing_file_paths()
        self.assertEqual(len(missing_files), 0)

    def test_file_tracking(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        paths = {'first.txt', 'second.txt', 'third.txt'}
        for path in paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'first.txt', 'second.txt', 'third.txt'})
        document_id = repository.track_file('second.txt')
        self.assertEqual(document_id, 1)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'first.txt', 'third.txt'})
        document_id = repository.track_file('third.txt')
        self.assertEqual(document_id, 2)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'first.txt'})
        document_id = repository.track_file('first.txt')
        self.assertEqual(document_id, 3)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, set())

    def test_document_untracking(self):
        database = Database(TEST_LOG_PATH)
        documents = [
            {
                'name': 'first.txt',
                'type': 'txt',
                'path': 'first.txt'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'images/second.png'
            },
            {
                'name': 'second.png',
                'type': 'png',
                'path': 'second.png'
            }
        ]
        for document in documents:
            database.create_document(**document)
        storage = Storage(TEST_ROOT_PATH)
        storage_paths = {'first.txt', 'images/second.png', 'second.png'}
        os.mkdir(TEST_ROOT_PATH + 'images')
        for path in storage_paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, set())
        repository.untrack_document(3)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'second.png'})
        repository.untrack_document(1)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'first.txt', 'second.png'})
        repository.untrack_document(2)
        untracked_files = repository.collect_untracked_file_paths()
        self.assertEqual(untracked_files, {'first.txt', 'images/second.png', 'second.png'})

    def test_track_untrack_and_track_again(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        storage_paths = {'alpha.py', 'beta.py'}
        for path in storage_paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        repository = Repository(database, storage)
        for _ in range(1, 10):
            untracked_files = repository.collect_untracked_file_paths()
            self.assertEqual(untracked_files, {'alpha.py', 'beta.py'})
            alpha_id = repository.track_file('alpha.py')
            untracked_files = repository.collect_untracked_file_paths()
            self.assertEqual(untracked_files, {'beta.py'})
            beta_id = repository.track_file('beta.py')
            untracked_files = repository.collect_untracked_file_paths()
            self.assertEqual(untracked_files, set())
            repository.untrack_document(alpha_id)
            untracked_files = repository.collect_untracked_file_paths()
            self.assertEqual(untracked_files, {'alpha.py'})
            repository.untrack_document(beta_id)

    def test_invalid_track(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        repository = Repository(database, storage)
        with self.assertRaises(ValueError):
            _ = repository.track_file('invalid/path.error')

    def test_invalid_untrack(self):
        database = Database(TEST_LOG_PATH)
        storage = Storage(TEST_ROOT_PATH)
        repository = Repository(database, storage)
        with self.assertRaises(ValueError):
            _ = repository.untrack_document(1234)
