import os
import unittest
from pg_fms.commands.file_operations import (
    move_file,
    copy_file,
    rename_file,
    delete_file,
    create_file,
    read_file,
    list_files,
    search_files,
)


class TestFileOperations(unittest.TestCase):

    def setUp(self):
        os.makedirs("test_dir", exist_ok=True)
        with open("test_dir/test_file.txt", "w", encoding="utf-8") as f:
            f.write("Hello, World!")

    def tearDown(self):
        if os.path.exists("test_dir"):
            for root, dirs, files in os.walk("test_dir", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir("test_dir")

    def test_create_file(self):
        create_file("test_dir/new_file.txt")
        self.assertTrue(os.path.exists("test_dir/new_file.txt"))

    def test_read_file(self):
        content = read_file("test_dir/test_file.txt")
        self.assertEqual(content, "Hello, World!")

    def test_move_file(self):
        move_file("test_dir/test_file.txt", "test_dir/moved_file.txt")
        self.assertTrue(os.path.exists("test_dir/moved_file.txt"))
        self.assertFalse(os.path.exists("test_dir/test_file.txt"))

    def test_copy_file(self):
        copy_file("test_dir/test_file.txt", "test_dir/copied_file.txt")
        self.assertTrue(os.path.exists("test_dir/copied_file.txt"))

    def test_rename_file(self):
        rename_file("test_dir/test_file.txt", "renamed_file.txt")
        self.assertTrue(os.path.exists("test_dir/renamed_file.txt"))
        self.assertFalse(os.path.exists("test_dir/test_file.txt"))

    def test_delete_file(self):
        delete_file("test_dir/test_file.txt")
        self.assertFalse(os.path.exists("test_dir/test_file.txt"))

    def test_list_files(self):
        files = list_files("test_dir")
        self.assertIn("test_file.txt", files)

    def test_search_files(self):
        matches = search_files("test_dir", "*.txt")
        self.assertIn("test_dir/test_file.txt", matches)


if __name__ == "__main__":
    unittest.main()
