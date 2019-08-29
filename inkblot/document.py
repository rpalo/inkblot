import markdown


class Document:
    def __init__(self, path, md=None):
        self.path = path
        if md is None:
            self.converter = markdown.Markdown()
        else:
            self.converter = md

    def __repr__(self):
        return f"Document(path={self.path})"

    @property
    def content(self):
        return self.path.read_text()

    def render(self):
        return self.converter.convert(self.content)
