import os
import subprocess
import unittest


class TestCLICommands(unittest.TestCase):
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

    def run_cli_command(self, command):
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout, result.stderr

    def test_create_file_cli(self):
        stdout, stderr = self.run_cli_command(
            "pg-fms create test_dir/cli_test_file.txt"
        )
        self.assertTrue(os.path.exists("test_dir/cli_test_file.txt"))
        self.assertEqual(stderr, "")

    def test_read_file_cli(self):
        stdout, stderr = self.run_cli_command("pg-fms read test_dir/test_file.txt")
        self.assertIn("Hello, World!", stdout)
        self.assertEqual(stderr, "")

    def test_move_file_cli(self):
        stdout, stderr = self.run_cli_command(
            "pg-fms move test_dir/test_file.txt test_dir/moved_file.txt"
        )
        self.assertTrue(os.path.exists("test_dir/moved_file.txt"))
        self.assertFalse(os.path.exists("test_dir/test_file.txt"))
        self.assertEqual(stderr, "")

    def test_copy_file_cli(self):
        stdout, stderr = self.run_cli_command(
            "pg-fms copy test_dir/test_file.txt test_dir/copied_file.txt"
        )
        self.assertTrue(os.path.exists("test_dir/copied_file.txt"))
        self.assertEqual(stderr, "")

    def test_delete_file_cli(self):
        stdout, stderr = self.run_cli_command("pg-fms delete test_dir/test_file.txt")
        self.assertFalse(os.path.exists("test_dir/test_file.txt"))
        self.assertEqual(stderr, "")

    def test_list_files_cli(self):
        stdout, stderr = self.run_cli_command("pg-fms list test_dir")
        self.assertIn("test_file.txt", stdout)
        self.assertEqual(stderr, "")


if __name__ == "__main__":
    unittest.main()
