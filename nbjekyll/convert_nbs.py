#!/usr/bin/env python
"""
Script for conversion of .ipynb files into a format suitable
for Jekyll blog posts
"""

import os

from pathlib import Path
from string import Template
import pytest
import argparse

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
    print("[nbjekyll] Running test on {}".format(os.path.split(nb)[1]))
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
        badge = 'validated-brightgreen.svg'
    elif exit_code == 1:
        validated = 'no'
        badge = 'validation failed-red.svg'
    else:
        validated = 'unknown'
        badge = 'unknown%20status-yellow.svg'
    return [validated, badge]

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

def parse_path():
    arg_parser = argparse.ArgumentParser(description="Convert Jupyter notebooks to Jekyll posts")
    arg_parser.add_argument('-p', '--path',
                            help="Custom path to save the Notebook images. The path in the"
                            " output markdown will be modified accordingly")

    return arg_parser.parse_args()

if __name__ == '__main__':
    args = parse_path()
    if args.path:
        img_path = args.path
    else:
        img_path = './images/notebook_images'

    print('[nbjekyll] Images will be saved in [{}]'.format(img_path))

    here = os.getcwd()

    # Step one: find if this is a repository
    repository = nb_repo(here)

    # Find the notebooks that have been added to the repo
    # or that have been updated in the last commit
    notebooks = repository.check_log()
    # Convert each of the notebooks using nbconvert
    # then add repo specific information
    for nb in notebooks['notebooks']:
        nb_path = Path(nb).resolve()
        if os.path.exists(nb_path):
            # convert the notebook in a .md
            print('[nbjekyll] Converting [{}]'.format(nb))
            jekyll_export.convert_single_nb(nb_path, img_path)
            # use nbval for the notebook
            test = validate_nb(nb_path)
            notebooks['validated'] = test[0]
            notebooks['badge'] = test[1]

            # substitute header
            format_template(notebooks, nb)
            print('[nbjekyll] Finalising conversion of [{}]'.format(nb))
