from setuptools import setup, find_packages
import os

name = 'nbjekyll'

pkg_root = os.path.join(os.path.dirname(__file__), name)
here = os.path.dirname(__file__)

packages = find_packages()

setup_args = dict(name = name,
                  version = '0.2',
                  description = 'Package used for custom conversion from Jupyter notebook to Jekyll posts',
                  url = 'https://github.com/trallard/nbconvert-jekyllconvert.git',
                  author = 'Tania Allard',
                  author_email = 't.allard@sheffield.ac.uk',
                  description_file = 'README.md',
                  license = 'MIT',
                  include_package_data = True,
                  packages = packages,
                  zip_safe = False,
                  install_requires = ['pygit2', 'nbval'])

if __name__ == '__main__':
    setup(**setup_args)
