import os
import unittest
from pg_fms.commands.file_operations import batch_operation


class TestBatchOperations(unittest.TestCase):

    def setUp(self):
        os.makedirs("test_dir", exist_ok=True)
        with open("test_dir/test_file1.txt", "w", encoding="utf-8") as f:
            f.write("File 1")
        with open("test_dir/test_file2.txt", "w", encoding="utf-8") as f:
            f.write("File 2")

    def tearDown(self):
        if os.path.exists("test_dir"):
            for root, dirs, files in os.walk("test_dir", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir("test_dir")

    def test_batch_move(self):
        os.makedirs("test_dir/moved_files", exist_ok=True)
        batch_operation(
            "move",
            ["test_dir/test_file1.txt", "test_dir/test_file2.txt"],
            "test_dir/moved_files",
        )
        self.assertTrue(os.path.exists("test_dir/moved_files/test_file1.txt"))
        self.assertTrue(os.path.exists("test_dir/moved_files/test_file2.txt"))

    def test_batch_copy(self):
        os.makedirs("test_dir/copied_files", exist_ok=True)
        batch_operation(
            "copy",
            ["test_dir/test_file1.txt", "test_dir/test_file2.txt"],
            "test_dir/copied_files",
        )
        self.assertTrue(os.path.exists("test_dir/copied_files/test_file1.txt"))
        self.assertTrue(os.path.exists("test_dir/copied_files/test_file2.txt"))

    def test_batch_delete(self):
        batch_operation(
            "delete", ["test_dir/test_file1.txt", "test_dir/test_file2.txt"]
        )
        self.assertFalse(os.path.exists("test_dir/test_file1.txt"))
        self.assertFalse(os.path.exists("test_dir/test_file2.txt"))


if __name__ == "__main__":
    unittest.main()
