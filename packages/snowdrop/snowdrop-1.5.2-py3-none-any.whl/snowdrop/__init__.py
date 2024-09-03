"""
Make snowdrop easier to import.
"""

__version__ = "1.5.2"
__all__ = ['html_renderer', 'ast_renderer', 'block_token', 'block_tokenizer',
           'span_token', 'span_tokenizer']

from snowdrop.block_token import Document
from snowdrop.html_renderer import HtmlRenderer
# import the old name for backwards compatibility:
from snowdrop.html_renderer import HTMLRenderer  # noqa: F401


def markdown(iterable, renderer=HtmlRenderer):
    """
    Converts markdown input to the output supported by the given renderer.
    If no renderer is supplied, ``HtmlRenderer`` is used.

    Note that extra token types supported by the given renderer
    are automatically (and temporarily) added to the parsing process.
    """
    with renderer() as renderer:
        return renderer.render(Document(iterable))
