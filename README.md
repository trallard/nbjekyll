# nbjekyll

[![Build Status](https://travis-ci.org/trallard/nbjekyll.svg?branch=master)](https://travis-ci.org/trallard/nbjekyll)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Build Status](https://travis-ci.org/trallard/nbjekyll.svg?branch=master)](https://travis-ci.org/trallard/nbjekyll)
[![PyPI](https://img.shields.io/pypi/v/nine.svg)](https://pypi.python.org/pypi/nbjekyll)

An experimental tool to convert Jupyter notebooks to .md files that could be immediately passed into Jekyll for publishing.

Jupyter comes with support for generating .md files by using their own generated exporters and templates. This is a very robust approach, but far from being ideal for .md conversion for Jekyll static blogs.

nbjekyll uses the nbconvert markdown exporter but ensures that the plots generated in the notebooks are saved in a separate directory and that the paths to such plots can be easily interpreted by Jekyll.
The path for the plots is by default specified as `./images/notebook_images/{Notebook_name}` but it can be modified if needed. For more details see [Usage](#usage).


nbjekylluses [nbval](https://github.com/computationalmodelling/nbval) to test the notebooks. Depending on the status code (see [pytest exit codes](https://docs.pytest.org/en/latest/usage.html)) the validation and appropriate badge is added:

![](https://img.shields.io/badge/notebook-validated-brightgreen.svg)

<img src="https://img.shields.io/badge/notebook-validation failed-red.svg">

![](https://img.shields.io/badge/notebook-unknown%20status-yellow.svg)

It returns a .md file with the yaml header needed for Jekyll. It contains the mandatory fields of `title` and `layout` (by default set to notebook). It also adds other fields such as the sha1 and author of the last commit associated to the notebook, the last update date, and a badge indicating if the notebook passed the validation with nbval.

```yaml
---
layout: notebook
title: "Classify_demo"
tags:
update_date: 17-01-2018
code_version: 19e3e29
author: Tania Allard
validation_pass: 'yes'
badge: "https://img.shields.io/badge/notebook-validated-brightgreen.svg"
---
```

You can see a Jekyll site using the converted notebooks  [here](http://bitsandchips.me/Modules-template/) ✨⚡️

## Install
nbjekyll is available from [PyPi](https://pypi.python.org/pypi/nbjekyll) so you can install nbjekyll using pip like so:
```bash
pip install nbjekyll
```

## Usage
Once the package is installed you can start using it directly from
your Jekyll site directory.

1. Add the Jupyter notebook you want to add to your blog
2. Commit the notebook or notebooks to Git
3. Run the Jekyll converter from the terminal. Make sure to run it from the
main directory of your Jekyll blog:

```bash
python -m nbjekyll.convert_nbs
```
If you want your output images to be in a different path you can use the flags `-p` `--path` like so:

```bash
python -m nbjekyll.convert_nbs -p ./site_images
```
4. Make sure to modify the layout in your .md yaml header!

## Important things to consider
- **You need to commit your notebooks to Git _right_ before using nbjekyll**

At this moment nbjekyll will check for the last commit in your repository and convert the notebooks associated to such commit.

We are looking into changing this to allow for more flexibility in the near future.

- **What are the pre requisites?**
  - Python > 3.4
  - pytest
  - nbval
  - nbconvert > 5.0
  - pygit2 (if you use conda the easiest way to get this installed is by doing `conda install -c conda-forge pygit2`)
