import os
from pathlib import Path
from utils.nb_git import nb_repo
from jekyllconvert import jekyll_export
import pytest

def validate_nb(nb):
    """It calls pytest with nbval to
    perform regression testing on each of the
    notebooks

    Parameters
        ----------
        nb: path
            path to the notebook to be tested

    Returns
        -------
        test: int
            exit code of the test
    """
    print("Running test on: {}".format(os.path.split(nb)[1]))
    return pytest.main([nb, '--nbval-lax'])


if __name__ == '__main__':
    here = os.path.dirname(__file__)
    #here = os.getcwd()
    repository = nb_repo(os.getcwd())
    notebooks = repository.check_log()
    print(notebooks)
    for nb in notebooks['notebooks']:
       nb_path = Path(nb).resolve()
       #jekyll_export.convert_single_nb(nb_path)
       #test = validate_nb(nb_path)
