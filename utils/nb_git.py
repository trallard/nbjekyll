import pygit2
import os

import fnmatch
import glob
from pathlib import Path

class nb_repo(object):
    """ Class containing methods used to
    identify the notebooks committed to the
    repository and add the SHA to the Jinja template"""

    def __init__(self, here):
        """ Find if the current location is a
        Git repository, if so it will return a
        repository object """
        try:
            repo_path = pygit2.discover_repository(here)
            repo = pygit2.Repository(repo_path)
            self.repo = repo
            self.here = here
        except:
            raise IOError ('This does not seem to be a repository')


    def check_log(self):
        """ Check the number of commits in the repository,
        if there is only one commit it will find all the notebooks.
        Otherwise it will find the notebooks in the latest commit only
        """
        all_commits = [commit for commit in self.repo.head.log()]
        if len(all_commits) <= 1:
            print('Only one commit: converting all notebooks')
            nb_coll = self.find_notebooks()
            sha1 = self.repo.revparse_single('HEAD').hex[0:7]
            notebooks = {'sha1': sha1,
                         'notebooks': nb_coll}
            return notebooks
        else:
            print(("There are notebooks already in version control,"
                   "finding the notebooks passed in the last commit"))
            notebooks = self.last_commit()
            return notebooks

    def find_notebooks(self):
        """ Find all the notebooks in the repo, but excludes those
        in the _site folder, this will be default if no specific
        notebook was passed for conversion
        """
        basePath = Path(os.getcwd())
        notebooksAll = [nb for nb in glob.glob('**/*.ipynb')]
        exception = os.path.join(basePath, '/_site/*/*')
        notebooks = [nb for nb in notebooksAll if not fnmatch.fnmatch(nb, exception)]

        if not(notebooks) == True:
            print('There were no notebooks found')
        else:
            return notebooks

    def last_commit(self):
        last = self.repo.revparse_single('HEAD')
        sha1 = last.hex[0:7]
        notebooks = [nb.name for nb in last.tree if '.ipynb' in nb.name]
        nb_coll = {'sha1': sha1,
                   'notebooks': notebooks}
        return nb_coll


