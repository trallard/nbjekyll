"""
This uses the Jekyll markdown exporter to convert .ipynb files
to .md files.
It ensures that the images are not saved as base64 but as separate
.png, .jpg. or .svg files in an images directory and that the
path to this is accurately updated using a custom jekyllpath filter

It also uses Beautiful soup to do some basic HTML parsing
"""
import os
import io

from traitlets.config import Config
from nbconvert import MarkdownExporter
from ipython_genutils.path import ensure_dir_exists

from bs4 import BeautifulSoup

def init_nb_resources(notebook_filename, img_path):
    """Step 1: Initialize resources
            This initializes the resources dictionary for a single notebook.
            Returns
            -------
            resources dictionary for a single notebook that MUST include:
                - unique_key: notebook nametable
    """
    resources = {}
    basename = os.path.basename(notebook_filename)
    notebook_name = basename[:basename.rfind('.')]
    resources['unique_key'] = notebook_name
    #resources['output_files_dir'] = './images/notebook_images/{}'.format(notebook_name)
    resources['output_files_dir'] = img_path + '/' +notebook_name
    return resources

def export_notebook(notebook_filename, resources):
    """Step 2: Export the notebook
        Exports the notebook to a particular format according to the specified
        exporter. This function returns the output and (possibly modified)
        resources from the exporter.
        Parameters
        ----------
        notebook_filename : str
            name of notebook file.
        resources : dict
        Returns
        -------
        output
        dict
            resources (possibly modified)
        """
    config = Config()
    basePath = os.path.dirname(__file__)
    exporter = MarkdownExporter(config = config,
                                template_path = [os.path.join(basePath,'templates/')],
                                template_file = 'Jekyll_template.tpl',
                                filters = {'jekyllpath': jekyllpath})
    content, resources = exporter.from_filename(notebook_filename, resources = resources)
    content = parse_html(content)
    return content, resources

def parse_html(content):
    """ This step is included in Step 2: this will use beautiful soup to
    modify certain tags of the returned content
    Parameters
    ----------
    content : returned from the notebook export
    Returns
    ------
    soup (parsed html content)
    """
    soup = BeautifulSoup(content, 'html.parser')
    if soup.table:
        for tag in soup.find_all('table'):
            tag['class'] = 'table-responsive table-striped'
            tag['border'] = '0'
    return soup


def jekyllpath(path):
    """ Take the filepath of an image output by the ExportOutputProcessor
    and convert it into a URL we can use with Jekyll. This is passed to the exporter
    as a filter to the exporter.
    Note that this will be directly taken from the Jekyll _config.yml file
    """
    return path.replace("./", "{{site.url}}{{site.baseurl}}/")

def write_outputs(content, resources):
    """Step 3: Write the notebook to file
            This writes output from the exporter to file using the specified writer.
            It returns the results from the writer.
            Parameters
            ----------
            output :
            resources : dict
                resources for a single notebook including name, config directory
                and directory to save output
            Returns
            -------
            file
                results from the specified writer output of exporter
            """

    # various paths and variables needed for the module
    notebook_namefull = resources['metadata']['name'] + resources.get('output_extension')
    outdir_nb = resources['metadata']['path']
    outfile = os.path.join(outdir_nb, notebook_namefull)
    imgs_outdir = resources.get('output_files_dir')
    ensure_dir_exists(imgs_outdir)

    # write file in the appropriate format
    with io.open(outfile, 'w', encoding = "utf-8") as fout:
        body = content.prettify(formatter='html')
        fout.write(body)

    # if the content has images then they are returned and saved
    if resources['outputs']:
        save_imgs(resources, imgs_outdir)

def save_imgs(resources, imgs_outdir):
    """ If the notebook had plots or figures, then they are saved in the appropriate
    directory"""
    items = resources.get('outputs', {}).items()
    if not os.path.exists(imgs_outdir):
        os.mkdir(imgs_outdir)
    for filename, data in items:
        dest = filename
        with io.open(dest, 'wb+') as f:
            f.write(data)

def convert_single_nb(notebook_filename, img_path):
    """Convert a single notebook.
            Performs the following steps:
                1. Initialize notebook resources
                2. Export the notebook to a particular format
                3. Write the exported notebook to file as well as complementary images
            Parameters
            ----------
            notebook_filename : str
            img_path : str
            """
    resources = init_nb_resources(notebook_filename, img_path)
    content, resources = export_notebook(notebook_filename, resources)
    write_outputs(content, resources)
