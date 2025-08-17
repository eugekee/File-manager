import unittest
import subprocess
import tempfile
import os
import shutil
import sys

PYTHON_EXECUTABLE = sys.executable

class TestManagerCLI(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def run_manager(self, *args):
        cmd = [PYTHON_EXECUTABLE, os.path.join(self.old_cwd, 'manager.py')] + list(args)
        proc = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        return proc.stdout.strip(), proc.stderr.strip(), proc.returncode

    def test_create_folder(self):
        out, err, code = self.run_manager('create', 'abc')
        self.assertIn('Папка создана', out)
        self.assertTrue(os.path.isdir('abc'))
        self.assertEqual(code, 0)

    def test_delete_folder(self):
        os.makedirs('todel')
        out, err, code = self.run_manager('delete', 'todel')
        self.assertIn('Папка удалена', out)
        self.assertFalse(os.path.exists('todel'))
        self.assertEqual(code, 0)

    def test_find_files(self):
        os.makedirs('dir1')
        with open('dir1/testfile.txt', 'w') as f:
            f.write('hello')
        out, err, code = self.run_manager('find', 'dir1', 'testfile')
        self.assertIn('testfile.txt', out)
        self.assertEqual(code, 0)

    def test_add_date_to_filename(self):
        with open('abc.txt', 'w') as f:
            f.write('test!')
        out, err, code = self.run_manager('adddate', 'abc.txt')
        self.assertIn('Переименовано', out)
        found_files = [x for x in os.listdir('.') if x.endswith('_abc.txt')]
        self.assertEqual(len(found_files), 1)
        self.assertEqual(code, 0)

    def test_help(self):
        out, err, code = self.run_manager('--help')
        self.assertIn('Менеджер файловой системы', out)
        self.assertEqual(code, 0)


if __name__ == '__main__':
    unittest.main()