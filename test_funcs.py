import unittest
import tempfile
from funcs import *

class TestFSFunctions(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_file = os.path.join(self.temp_dir, 'test.txt')
        with open(self.temp_file, 'w') as f:
            f.write('123')

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_create_folder(self):
        path = os.path.join(self.temp_dir, 'new_folder')
        msg = create_folder(path)
        self.assertTrue(os.path.isdir(path))
        self.assertIn('Папка создана', msg)

    def test_delete_path_file(self):
        msg = delete_path(self.temp_file)
        self.assertFalse(os.path.exists(self.temp_file))
        self.assertIn('Файл удалён', msg)

    def test_delete_path_dir(self):
        msg = delete_path(self.temp_dir)
        self.assertFalse(os.path.exists(self.temp_dir))
        self.assertIn('Папка удалена', msg)

    def test_find_files_by_regex(self):
        res = find_files_by_regex(self.temp_dir, r'test.*\.txt')
        self.assertIn(self.temp_file, res)

    def test_add_date_to_filenames(self):
        files = add_date_to_filenames(self.temp_file)
        self.assertEqual(len(files), 1)
        self.assertTrue(os.path.exists(files[0]))
        self.assertRegex(os.path.basename(files[0]), r'^\d+_test\.txt$')

if __name__ == '__main__':
    unittest.main()