import unittest
import os


class TestSecurity(unittest.TestCase):

    def test_file_permissions(self):
        test_file = "test_security_file.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("Test content")

        os.chmod(test_file, 0o444)

        file_stat = os.stat(test_file)
        self.assertEqual(oct(file_stat.st_mode)[-3:], "444")

        os.remove(test_file)

    def test_directory_permissions(self):
        test_dir = "test_security_dir"
        os.mkdir(test_dir)

        os.chmod(test_dir, 0o555)

        dir_stat = os.stat(test_dir)
        self.assertEqual(oct(dir_stat.st_mode)[-3:], "555")

        os.rmdir(test_dir)


if __name__ == "__main__":
    unittest.main()
