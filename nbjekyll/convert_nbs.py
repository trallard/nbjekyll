#!/usr/bin/env python
"""
Script for conversion of .ipynb files into a format suitable
for Jekyll blog posts
"""

import os
from pathlib import Path
from string import Template
import pytest

from .nb_git.nb_git import nb_repo
from .jekyllconvert import jekyll_export


#-----------------------------------------------------------------------------
#Classes and functions
#-----------------------------------------------------------------------------

def validate_nb(nb):
    """
    Run pytest with nbval on the notebooks
    :param nb:
    :return: pytest exit code
    see hhttps://docs.pytest.org/en/latest/usage.html?%20main
    """
    print("Running test on: {}".format(os.path.split(nb)[1]))
    return validation_code(pytest.main([nb, '--nbval-lax']))


def validation_code(exit_code):
    """
    Check the exit code and pass the value to
    the dictionary containing the commit information
    :param exit_code:
    :return: validation status
    """
    if exit_code == 0:
        validated = 'yes'
    elif exit_code == 1:
        validated = 'no'
    else:
        validated = 'unknown'
    return validated


def format_template(commit_info, nb):
    """
    Replace the template data with the information
    collected from the commit before
    :param commit_info:
    :param nb:
    :return: modified .md for the notebook previously
    converted
    """

    nb_path = os.path.abspath(nb).replace('ipynb', 'md')
    with open(nb_path, 'r+') as file:
        template = NbTemplate(file.read())
        updated = template.substitute(commit_info)
        file.seek(0)
        file.write(updated)
        file.truncate()


class NbTemplate(Template):
    """"
    Subclass of Template, this uses [- -] as the delimiter sequence
    to replace the template variables instead of the default $, ${}, $$
    as this causes problems when then notebooks use the R kernel
    """
    delimiter = '[-'
    pattern = r'''
        \[-(?:
           (?P<escaped>-) |            # Expression [-- will become [-
           (?P<named>[^\[\]\n-]+)-\] | # -, [, ], and \n can't be used in names
           \b\B(?P<braced>) |          # Braced names disabled
           (?P<invalid>)               #
        )
        '''


if __name__ == '__main__':
    """ Will use the as base path """
    here = os.getcwd()
    print(here)

    # Step one: find if this is a repository
    repository = nb_repo(os.getcwd())

    # Find the notebooks that have been added to the repo
    # or that have been updated in the last commit
    notebooks = repository.check_log()
    print(notebooks)

    # Convert each of the notebooks using nbconvert
    # then add repo specific information
    for nb in notebooks['notebooks']:
        # convert the notebook in a .md
        print('Converting {}'.format(nb))
        nb_path = Path(nb).resolve()
        jekyll_export.convert_single_nb(nb_path)

        # use nbval for the notebook
        #test = validate_nb(nb_path)
        #notebooks['validated'] = test

        # substitute header
        format_template(notebooks, nb)
        print('*****Finalising conversion')
