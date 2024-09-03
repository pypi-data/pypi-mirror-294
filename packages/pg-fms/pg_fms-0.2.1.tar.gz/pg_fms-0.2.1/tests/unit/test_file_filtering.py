import os
import unittest
from datetime import datetime, timedelta
from pg_fms.commands.file_filtering import (
    filter_by_type,
    filter_by_size,
    filter_by_date_modified,
)


class TestFileFiltering(unittest.TestCase):

    def setUp(self):
        os.makedirs("test_dir", exist_ok=True)
        with open("test_dir/test_file1.txt", "w", encoding="utf-8") as f:
            f.write("File 1")
        with open("test_dir/test_file2.log", "w", encoding="utf-8") as f:
            f.write("File 2")
        with open("test_dir/test_file3.txt", "w", encoding="utf-8") as f:
            f.write("File 3")
        with open("test_dir/test_file4.txt", "w", encoding="utf-8") as f:
            f.write("File 4")
        with open("test_dir/test_file5.log", "w", encoding="utf-8") as f:
            f.write("File 5")

        # Set file sizes
        with open("test_dir/small_file.txt", "w", encoding="utf-8") as f:
            f.write("small")
        with open("test_dir/large_file.txt", "w", encoding="utf-8") as f:
            f.write("large" * 1000)

        # Set file modification times
        old_time = datetime.now() - timedelta(days=10)
        os.utime(
            "test_dir/test_file1.txt", (old_time.timestamp(), old_time.timestamp())
        )
        os.utime(
            "test_dir/test_file2.log", (old_time.timestamp(), old_time.timestamp())
        )

    def tearDown(self):
        if os.path.exists("test_dir"):
            for root, dirs, files in os.walk("test_dir", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir("test_dir")

    def test_filter_by_type(self):
        txt_files = filter_by_type("test_dir", ".txt")
        self.assertIn("test_file1.txt", txt_files)
        self.assertIn("test_file3.txt", txt_files)
        self.assertIn("test_file4.txt", txt_files)
        self.assertNotIn("test_file2.log", txt_files)
        self.assertNotIn("test_file5.log", txt_files)

    def test_filter_by_size(self):
        size_filtered_files = filter_by_size("test_dir", 0, 100)
        self.assertIn("small_file.txt", size_filtered_files)
        self.assertNotIn("large_file.txt", size_filtered_files)

    def test_filter_by_date_modified(self):
        recent_files = filter_by_date_modified("test_dir", 5)
        self.assertIn("test_file3.txt", recent_files)
        self.assertIn("test_file4.txt", recent_files)
        self.assertNotIn("test_file1.txt", recent_files)
        self.assertNotIn("test_file2.log", recent_files)


if __name__ == "__main__":
    unittest.main()
