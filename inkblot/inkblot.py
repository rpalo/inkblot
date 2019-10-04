from functools import partial
from itertools import chain
import pathlib
import shutil

import jinja2
import markdown

from inkblot import converters
from inkblot.document import Document
from inkblot.document_loader import DocumentLoader


def generate(directory: pathlib.Path, config):
    md = markdown.Markdown()
    outputs = {}
    supports = {}
    source_dir = directory / config["source_dir"]

    for f in source_dir.rglob(f"*.*"):
        doc = Document(f, base=source_dir)
        if any(part.startswith("_") for part in doc.path.parts):
            supports[doc.path.as_posix()] = doc
        else:
            outputs[doc.path.as_posix()] = doc

    support_loader = DocumentLoader(supports)
    output_loader = DocumentLoader(outputs)
    loader = jinja2.ChoiceLoader([support_loader, output_loader])

    env = jinja2.Environment(
        loader=loader, autoescape=jinja2.select_autoescape(["html", "xml"])
    )

    @converters.converter
    def jinjafy(doc):
        template = env.get_template(doc.path.as_posix())
        try:
            doc.body = template.render(doc.attributes)
        except jinja2.exceptions.TemplateAssertionError:
            print("FAILED:\n\n" + doc.body)
        return doc

    output_path = directory / config["build_dir"]
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()

    config["conversions"].update(config["extra_conversions"])
    for doc in outputs.values():
        for name in config["conversions"][doc.suffix]:
            converters.conversions[name](doc)

        path = output_path / doc.path.with_suffix(doc.suffix)
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_text(doc.body)
