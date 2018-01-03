import os
from pathlib import Path
from utils.nb_git import nb_repo
from jekyllconvert import jekyll_export
import pytest

def validate_nb(nb):
    """It calls pytest with nbval to
    perform regression testing on each of the
    notebooks
    """
    print("Running test")
    pytest.main([nb, '--nbval-lax'])


if __name__ == '__main__':
    here = os.path.dirname(__file__)
    here = os.getcwd()
    repository = nb_repo(os.getcwd())
    notebooks = repository.check_log()
    for nb in notebooks['notebooks']:
       nb_path = Path(nb).resolve()
       #print(nb_path)
       #jekyll_export.convert_single_nb(nb_path)