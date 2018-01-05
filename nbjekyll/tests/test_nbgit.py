"""Tests the nb_git functions """


import unittest
from nbjekyll import nb_git
import pygit2
from . import utils
import os


class DiscoverRepositoryTest(utils.NoRepoTestCase):

    def test_discover_repo(self):
        repo = pygit2.init_repository(self._temp_dir, False)
        subdir = os.path.join(self._temp_dir, "test1", "test2")
        os.makedirs(subdir)
        self.assertEqual(repo.path, pygit2.discover_repository(subdir))




if __name__ == '__main__':
    unittest.main()