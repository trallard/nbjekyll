import os

from setuptools import setup, find_packages

name = 'nbjekyll'

pkg_root = os.path.join(os.path.dirname(__file__), name)
here = os.path.dirname(__file__)

setup_args = dict(name = name,
                  version = '0.1.1',

                  description = 'Package used for easy conversion from Jupyter notebook to Jekyll posts',
                  long_description = open('README.md').read(),

                  url = 'https://github.com/trallard/nbconvert-jekyllconvert.git',
                  donwload_url ='https://github.com/trallard/nbjekyll/archive/v0.1.1.tar.gz',

                  # Author details
                  author = 'Tania Allard',
                  author_email = 'taniar.allard@gmail.com',

                  license = 'MIT',
                  include_package_data = True,

                  # You can just specify the packages manually here if your project is
                  # simple. Or you can use find_packages().
                  packages = find_packages(),
                  zip_safe = False,

                  install_requires = ['pygit2', 'nbval', 'nbconvert >= 5.0','pytz'],

                  keywords =  'jupyter, jekyll, teaching, dissemination, open science',

                  classifiers = [
                    # Specify the Python versions you support here. In particular, ensure
                    # that you indicate whether you support Python 2, Python 3 or both.
                    'Programming Language :: Python :: 2',
                    'Programming Language :: Python :: 2.6',
                    'Programming Language :: Python :: 2.7',
                    'Programming Language :: Python :: 3',
                    'Programming Language :: Python :: 3.2',
                    'Programming Language :: Python :: 3.3',
                    'Programming Language :: Python :: 3.4',
                    'Programming Language :: Python :: 3.5',
                    'Programming Language :: Python :: 3.6',
                    "Development Status :: 3 - Alpha",
                    "Intended Audience :: Education",
                    "License :: OSI Approved :: MIT License" ] )

if __name__ == '__main__':
    setup(**setup_args)
