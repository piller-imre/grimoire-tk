import os
import shutil
import unittest

from grimoire.storage import Storage

TEST_ROOT_PATH = '/tmp/grimoire_test_storage/'


def touch(path, times=None):
    """A Python implementation of the touch command."""
    with open(path, 'a'):
        os.utime(path, times)


class StorageTest(unittest.TestCase):
    """Unittests for the storage class"""

    def setUp(self):
        """Remove the storage directory if exists."""
        try:
            shutil.rmtree(TEST_ROOT_PATH)
        except FileNotFoundError:
            pass

    def test_missing_root_path(self):
        self.assertFalse(os.path.isdir(TEST_ROOT_PATH))
        storage = Storage(path=TEST_ROOT_PATH)
        self.assertTrue(os.path.isdir(TEST_ROOT_PATH))

    def test_collect_file_paths_from_empty_storage(self):
        storage = Storage(path=TEST_ROOT_PATH)
        paths = storage.collect_file_paths()
        self.assertEqual(paths, [])

    def test_flat_file_layout(self):
        os.makedirs(TEST_ROOT_PATH)
        paths = ['sample_{}.txt'.format(i) for i in range(1, 11)]
        for path in paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        storage = Storage(path=TEST_ROOT_PATH)
        result_paths = storage.collect_file_paths()
        self.assertEqual(result_paths, paths)

    def test_directory_structure(self):
        os.makedirs(TEST_ROOT_PATH)
        for directory_name in ['images', 'musics', 'videos']:
            os.makedirs(TEST_ROOT_PATH + directory_name)
        note_paths = ['note_{}'.format(i) for i in range(4)]
        image_paths = ['images/image_{}.png'.format(i) for i in range(1, 24)]
        music_paths = ['musics/track_{}.ogg'.format(i) for i in range(32)]
        video_paths = ['videos/video_{}.mp4'.format(i) for i in range(8)]
        paths = note_paths + image_paths + music_paths + video_paths
        for path in paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        storage = Storage(path=TEST_ROOT_PATH)
        result_paths = storage.collect_file_paths()
        self.assertEqual(result_paths, paths)

    def test_empty_directory_skipping(self):
        os.makedirs(TEST_ROOT_PATH)
        paths = ['sample_{}.txt'.format(i) for i in range(1, 11)]
        for path in paths:
            absolute_path = TEST_ROOT_PATH + path
            touch(absolute_path)
        for directory_name in ['some', 'empty', 'directory']:
            os.makedirs(TEST_ROOT_PATH + directory_name)
        storage = Storage(path=TEST_ROOT_PATH)
        result_paths = storage.collect_file_paths()
        self.assertEqual(result_paths, paths)
