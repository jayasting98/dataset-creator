import os
import subprocess
import tempfile
import unittest

from dataset_creator import repositories


class MavenRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self._repo_dir_pathname = os.path.join('integration_tests',
            'resources', 'repositories', 'guess-the-number')
        self._repo = repositories.MavenRepository(self._repo_dir_pathname)

    def test_compile__typical_case__compiles(self):
        self._repo.compile()
        build_dir = os.path.join(self._repo_dir_pathname, 'target')
        self.assertTrue(os.path.isdir(build_dir))

    def test_compile__fails__raises_error(self):
        with tempfile.TemporaryDirectory() as dir:
            repo = repositories.MavenRepository(dir)
            with self.assertRaises(subprocess.CalledProcessError):
                repo.compile()
