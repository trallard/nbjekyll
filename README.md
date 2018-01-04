# nbconvert-jekyllconvert

An experimental tool to convert Jupyter notebooks to .md files that could be immediately passed into Jekyll for publishing.

Jupyter comes with support for generating .md files by using their own generated exporters and templates. This is a very robust approach, but far from being ideal for .md conversion for Jekyll static blogs.

jekyllconvert uses the nbconvert markdown exporter but ensures that the plots generated in the notebooks are saved in a separate directory.
This is by default specified as `./images/notebook_images/{Notebook_name}` but can be modified if needed.

Also, it adds a custom header displaying the version of the notebook (commit sha1), the date when it was last updated, and the author name.

It also uses [nbval](https://github.com/computationalmodelling/nbval) to test the notebooks. Depending on the status code (see [pytest exit codes](https://docs.pytest.org/en/latest/usage.html)) the validation and appropriate badge is added:

![](https://img.shields.io/badge/notebook-validated-brightgreen.svg)

<img src="https://img.shields.io/badge/notebook-validation failed-red.svg">

![](https://img.shields.io/badge/notebook-unknown%20status-yellow.svg)
