from functools import partial
from itertools import chain
import pathlib
import shutil

import jinja2
import markdown

from inkblot import converters
from inkblot.document import Document
from inkblot.document_loader import DocumentLoader


def generate(directory: pathlib.Path):
    md = markdown.Markdown()
    outputs = {}
    supports = {}

    target_suffixes = ["md", "html"]
    for f in chain.from_iterable(
        directory.rglob(f"*.{suff}") for suff in target_suffixes
    ):
        doc = Document(f, base=directory)
        if any(part.startswith("_") for part in doc.path.parts):
            supports[str(doc.path)] = doc
        else:
            outputs[str(doc.path)] = doc

    support_loader = DocumentLoader(supports)
    output_loader = DocumentLoader(outputs)
    loader = jinja2.ChoiceLoader([support_loader, output_loader])

    env = jinja2.Environment(
        loader=loader, autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    output_path = directory.parent / "output"
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()

    for doc in outputs.values():
        if doc.suffix == ".md":
            converters.md_to_html(doc)
        if "layout" in doc.attributes:
            converters.add_layout(doc)
        converters.jinjafy(doc, env=env)

        path = output_path / doc.path.with_suffix(doc.suffix)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_text(doc.body)
