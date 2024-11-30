import unittest
import os
import zipfile  # Не забывайте импортировать zipfile
from main import load_vfs, list_directory, change_directory, reverse_string, chmod_file, process_command

class TestVirtualShellEmulator(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовой виртуальной файловой системы."""
        self.test_vfs_path = "test_vfs.zip"
        self.vfs_content = {
            "main/": {"type": "dir", "permissions": "rwx"},
            "main/file1.txt": {"type": "file", "content": b"hello", "permissions": "rw"},
            "main/file2.txt": {"type": "file", "content": b"world", "permissions": "rw"},
            "main/root/": {"type": "dir", "permissions": "rwx"},
        }

        # Создание тестового zip-архива
        with zipfile.ZipFile(self.test_vfs_path, "w") as z:
            for path, meta in self.vfs_content.items():
                if meta["type"] == "dir":
                    z.writestr(path, "")
                else:
                    z.writestr(path, meta["content"])

        load_vfs(self.test_vfs_path)

    def tearDown(self):
        """Удаление тестового архива."""
        if os.path.exists(self.test_vfs_path):
            os.remove(self.test_vfs_path)

    def test_list_directory(self):
        """Тест команды ls."""
        self.assertEqual(list_directory(), "file1.txt\nfile2.txt\nroot")

    def test_change_directory(self):
        """Тест команды cd."""
        self.assertEqual(change_directory("root"), "Changed directory to: main/root/")
        self.assertEqual(change_directory(".."), "Changed directory to: main/")
        self.assertEqual(change_directory("nonexistent"), "Directory does not exist.")

    def test_reverse_string(self):
        """Тест команды rev."""
        self.assertEqual(reverse_string("hello"), "Reversed: olleh")
        self.assertEqual(reverse_string("12345"), "Reversed: 54321")

    def test_chmod_file(self):
        """Тест команды chmod."""
        self.assertEqual(chmod_file("file1.txt", "r--"), "Changed permissions of file1.txt to r--.")
        self.assertEqual(chmod_file("nonexistent.txt", "r--"), "Error: File or directory not found.")

    def test_process_command(self):
        """Тестируем общую обработку команд."""
        global current_path, vfs
        current_path = "main/"
        vfs = {
            "main/file1.txt": {"type": "file", "content": b"", "permissions": "rw"}
        }
        self.assertEqual(process_command("chmod file1.txt rw-"), "Changed permissions of file1.txt to rw-.")

    def test_edge_cases(self):
        global current_path
        current_path = "/"  # Устанавливаем корень
        self.assertEqual(change_directory(".."), "Changed directory to: /")  # Теперь должно работать корректно



if __name__ == "__main__":
    unittest.main()
