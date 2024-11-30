import unittest
from unittest.mock import patch, MagicMock
from graph_generator import get_commits

class TestDependencyVisualizerFake(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_commits_fake(self, mock_run):
        
        mock_result = MagicMock()
        mock_result.stdout = "abc123 Fake commit\nbcd234 Another fake commit"
        mock_run.return_value = mock_result

        repository_path = "/path/to/repo"
        file_hash = "example.txt"
        commits = get_commits(repository_path, file_hash)

        expected_commits = [
            ("abc123", "Fake commit"),
            ("bcd234", "Another fake commit")
        ]
        self.assertEqual(commits, expected_commits)

if __name__ == "__main__":
    unittest.main()
