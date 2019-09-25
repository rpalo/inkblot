"""Converters convert document bodies from one text format to another.

They are just functions that accept a Document and return a modified Document.
"""

from markdown import Markdown

from inkblot import document


def add_layout(doc: document.Document):
    if "layout" not in doc.attributes:
        raise ValueError("No layout in frontmatter.")
    doc.body = '{% extends "_layouts/' + doc.layout + '.html" %}\n' + doc.body
    return doc


def md_to_html(doc: document.Document, md=None):
    md = md or Markdown()
    doc.body = (
        "{% block content %}\n" + md.convert(doc.body) + "{% endblock content %}\n"
    )
    doc.suffix = ".html"
    return doc


def jinjafy(doc: document.Document, env):
    template = env.get_template(str(doc.path))
    doc.body = template.render(doc.attributes)
    return doc
