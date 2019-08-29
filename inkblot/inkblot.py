import pathlib
import shutil

import jinja2
import markdown


def generate(directory: pathlib.Path):
    md = markdown.Markdown()
    outputs = []

    for f in directory.iterdir():
        outputs.append((f.stem, md.reset().convert(f.read_text())))

    output_path = directory.parent / "output"
    if output_path.exists():
        shutil.rmtree(output_path)

    output_path.mkdir()
    for basename, html in outputs:
        (output_path / f"{basename}.html").write_text(html)
