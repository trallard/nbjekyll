import os
from pathlib import Path
from utils.nb_git import nb_repo
from jekyllconvert import jekyll_export
import pytest


def validate_nb(nb):
    """
    Run pytest with nbval on the notebooks
    :param nb:
    :return: pytest exit code
    see hhttps://docs.pytest.org/en/latest/usage.html?%20main
    """
    print("Running test on: {}".format(os.path.split(nb)[1]))
    return pytest.main([nb, '--nbval-lax'])


def validation_code(exit_code, notebooks):
    """
    Check the exit code and pass the value to
    the dictionary containing the commit information
    :param exit_code:
    :param notebooks:
    :return: modified dictionary
    """
    if exit_code == 0:
        notebooks['validated'] = 'yes'
    elif exit_code == 1:
        notebooks['validated'] = 'no'
    else:
        notebooks['validated'] = 'unknown'
    return notebooks


def format_template(commit_info, nb):
    """
    Replace the template data with the information
    collected from the commit before
    :param commit_info:
    :param nb:
    :return: modified .md for the notebook previously
    converted
    """
    from string import Template

    nb_path = os.path.abspath(nb).replace('ipynb', 'md')
    template = Template(open(nb_path, 'r').read())

    return template.substitute(commit_info)


if __name__ == '__main__':
    here = os.path.dirname(__file__)
    # here = os.getcwd()
    repository = nb_repo(os.getcwd())
    notebooks = repository.check_log()
    print(notebooks)
    for nb in notebooks['notebooks']:
        nb_path = Path(nb).resolve()
        jekyll_export.convert_single_nb(nb_path)
        # test = validate_nb(nb_path)
        format_template(notebooks, nb)
