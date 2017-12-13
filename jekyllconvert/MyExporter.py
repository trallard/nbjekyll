# file __init__.py
import os
import os.path


from traitlets import default, Unicode
from traitlets.config import Config

from nbconvert.filters.highlight import Highlight2HTML
from nbconvert.filters.markdown_mistune import IPythonRenderer, MarkdownWithMath

from nbconvert.exporters.html import HTMLExporter



#-----------------------------------------------------------------------------
# Classes
#-----------------------------------------------------------------------------

class MyExporter(HTMLExporter):
    """
    My custom exporter
    """

    anchor_link_text = Unicode(u'¶', help="The text used as the text for anchor links.").tag(config=True)
    output_mimetype = 'text/markdown'

    def _file_extension_default(self):
        """
        The new file extension is `.test_ext`
        """
        return '.md'

    @property
    def template_path(self):
        """
        We want to inherit from HTML template, and have template under
        `./templates/` so append it to the search path. (see next section)
        """
        #return super().template_path+[os.path.join(os.path.dirname(__file__), "templates")]
        module_path = os.path.join(os.path.dirname(__file__), "templates")
        print(module_path)
        return super().template_path + [module_path]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return 'test_template'

    @property
    def default_config(self):
        c = Config({
            'NbConvertBase': {
                'display_data_priority': ['application/vnd.jupyter.widget-state+json',
                                          'application/vnd.jupyter.widget-view+json',
                                          'application/javascript',
                                          'text/html',
                                          'text/markdown',
                                          'image/svg+xml',
                                          'text/latex',
                                          'image/png',
                                          'image/jpeg',
                                          'text/plain'
                                          ]
            },
            'CSSHTMLHeaderPreprocessor': {
                'enabled': True
            },
            'HighlightMagicsPreprocessor': {
                'enabled': True
            }
        })
        c.merge(super(HTMLExporter, self).default_config)
        return c

