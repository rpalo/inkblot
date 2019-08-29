import pathlib
import shutil

import jinja2
import markdown

from inkblot.document import Document


def generate(directory: pathlib.Path):
    md = markdown.Markdown()
    outputs = []

    for f in directory.glob("**/*.md"):
        outputs.append(Document(f))

    output_path = directory.parent / "output"
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir()

    for doc in outputs:
        relative = doc.path.relative_to(directory)
        path = output_path / relative.parent / f"{relative.stem}.html"
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        path.write_text(doc.render())
