"""Converters convert document bodies from one text format to another.

They are just functions that accept a Document and return a modified Document.
"""

from markdown import Markdown
import sass

from inkblot import document


conversions = dict()

def converter(func):
    conversions[func.__name__] = func
    return func

@converter
def md_to_html(doc: document.Document, md=None) -> document.Document:
    md = md or Markdown()
    doc.body = (
        "{% block content %}\n" + md.convert(doc.body) + "{% endblock content %}\n"
    )
    doc.suffix = ".html"
    return doc


@converter
def add_layout(doc: document.Document) -> document.Document:
    if "layout" not in doc.attributes:
        return doc
    doc.body = '{% extends "_layouts/' + doc.layout + '.html" %}\n' + doc.body
    return doc


# @converter
# def jinjafy(doc: document.Document, env) -> document.Document:
#     template = env.get_template(doc.path.as_posix())
#     doc.body = template.render(doc.attributes)
#     return doc


@converter
def compile_sass(doc: document.Document) -> document.Document:
    doc.body = sass.compile(string=doc.body, indented=True)
    doc.suffix = ".css"
    return doc