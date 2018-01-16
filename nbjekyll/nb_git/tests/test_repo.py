"""Tests the nb_git functions """
import os
import unittest
import pygit2
import pytest
import time
import datetime

from . import base

from ..nb_git import nb_repo

here = os.getcwd()

class RepoTest(base.NoRepoTestCase):

    def test_discover_repo(self):
        repo = pygit2.init_repository(self._temp_dir, False)
        subdir = os.path.join(self._temp_dir, "test1", "test2")
        os.makedirs(subdir)
        self.assertEqual(repo.path, pygit2.discover_repository(subdir))


def test_nb_repo():
    """ Checks a repo is found """
    repo = nb_repo(here)
    assert repo.repo.path == pygit2.discover_repository(here)

def test_find_notebooks():
    """Checks that the method finds the notebooks
    in this repository """
    notebooks = nb_repo(os.getcwd()).find_notebooks()
    assert len(notebooks) == 1
    assert notebooks[0] == 'Tutorial.ipynb'

def test_get_commit():
    """Tests the get commit function, does it return a commit?
    """
    last_commit = nb_repo(os.getcwd()).get_commit()
    repository = pygit2.Repository(pygit2.discover_repository(here))
    assert last_commit['sha1'] == repository.revparse_single('HEAD').hex[0:7]

def test_convert_time():
    now = time.time()
    conv_time = nb_repo(os.getcwd()).convert_time(now)
    now_full = datetime.datetime.now().strftime("%d-%m-%Y")
    assert conv_time == now_full


if __name__ == '__main__':
    unittest.main()