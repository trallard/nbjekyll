# -*- coding: utf-8 -*-
"""
Custom Markdown template for Jekyll purposes
Adapted from the HTML / markdown Exporters
Distributed under the terms of the Modified BSD License.

"""

import os
import path

from traitlets import default, Unicode
from traitlets.config import Config

from nbconvert.filters.highlight import Highlight2HTML
from nbconvert.filters.markdown_mistune import IPythonRenderer, MarkdownWithMath

from nbconvert.exporters.html import HTMLExporter


class JekyllExporter(HTMLExporter):
    """
    Exports a basic HTML document.  This exporter assists with the export of
    HTML.  Inherit from it if you are writing your own HTML template and need
    custom preprocessors/filters.  If you don't need custom preprocessors/
    filters, just change the 'template_file' config option.
    """

    anchor_link_text = Unicode(u'¶', help="The text used as the text for anchor links.").tag(config=True)

    output_mimetype = 'text/markdown'

    def _file_extension_default(self):
        """The exporter will return a .md file"""
        return '.md'

    @property
    def template_path(self):
        """
        We want to inherit from HTML template, and have  the template under
        `./templates/` so append it to the search path. (see next section)
        """
        return super().template_path+[os.path.join(os.path.dirname(__file__), "templates")]

    def _template_file_default(self):
        """
        We want to use the new template we ship with our library.
        """
        return  'jekyll_html'

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

    def markdown2html(self, source):
        """Markdown to HTML filter respecting the anchor_link_text setting"""
        renderer = IPythonRenderer(escape=False,
                                   anchor_link_text=self.anchor_link_text)
        return MarkdownWithMath(renderer=renderer).render(source)

    def default_filters(self):
        for pair in super(HTMLExporter, self).default_filters():
            yield pair
        yield ('markdown2html', self.markdown2html)

    def from_notebook_node(self, nb, resources=None, **kw):
        langinfo = nb.metadata.get('language_info', {})
        lexer = langinfo.get('pygments_lexer', langinfo.get('name', None))
        self.register_filter('highlight_code',
                             Highlight2HTML(pygments_lexer=lexer, parent=self))
        return super(HTMLExporter, self).from_notebook_node(nb, resources, **kw)
