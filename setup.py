from setuptools import setup
import os

name = 'jekyllconvert'

pkg_root = os.path.join(os.path.dirname(__file__), name)
here = os.path.dirname(__file__)

packages = []
for d, _, _ in os.walk(os.path.join(here, name)):
    if os.path.exists(os.path.join(d, '__init__.py')):
        packages.append(d[len(here)+1:].replace(os.path.sep, '.'))


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
                  install_requires = ['pygit2'])

if __name__ == '__main__':
    setup(**setup_args)
