import os
import timeit
import unittest
from pg_fms.commands.file_operations import (
    move_file,
    copy_file,
    delete_file,
    create_file,
    read_file,
    list_files,
)


class TestPerformance(unittest.TestCase):

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

    def test_create_file_performance(self):
        execution_time = timeit.timeit(
            lambda: create_file("test_dir/perf_test_file.txt"), number=100
        )
        print(f"Create file performance: {execution_time:.4f} seconds")

    def test_read_file_performance(self):
        execution_time = timeit.timeit(
            lambda: read_file("test_dir/test_file.txt"), number=100
        )
        print(f"Read file performance: {execution_time:.4f} seconds")

    def test_move_file_performance(self):
        execution_time = timeit.timeit(
            lambda: move_file("test_dir/test_file.txt", "test_dir/moved_file.txt"),
            number=100,
        )
        print(f"Move file performance: {execution_time:.4f} seconds")

    def test_copy_file_performance(self):
        execution_time = timeit.timeit(
            lambda: copy_file("test_dir/test_file.txt", "test_dir/copied_file.txt"),
            number=100,
        )
        print(f"Copy file performance: {execution_time:.4f} seconds")

    def test_delete_file_performance(self):
        execution_time = timeit.timeit(
            lambda: delete_file("test_dir/test_file.txt"), number=100
        )
        print(f"Delete file performance: {execution_time:.4f} seconds")

    def test_list_files_performance(self):
        execution_time = timeit.timeit(lambda: list_files("test_dir"), number=100)
        print(f"List files performance: {execution_time:.4f} seconds")


if __name__ == "__main__":
    unittest.main()
