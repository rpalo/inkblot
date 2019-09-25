class Document:
    def __init__(self, path, base=None, md=None):
        content = path.read_text()
        self.attributes = self.parse(content)
        if base is not None:
            self.path = path.relative_to(base)
        else:
            self.path = path

        self.suffix = self.path.suffix

    def __repr__(self):
        return f"Document(path={self.path}, attributes={self.attributes})"

    def __getattr__(self, name):
        if name in self.attributes:
            return self.attributes[name]
        else:
            raise AttributeError(f"{self} has no attribute {name}")

    @staticmethod
    def parse(text):
        header = "BEFORE"
        attributes = {}
        body = []

        if not text.startswith("---"):
            header = "AFTER"

        for line in text.splitlines():
            if line.startswith("---") and header == "BEFORE":
                header = "INSIDE"
                continue
            if line.startswith("---") and header == "INSIDE":
                header = "AFTER"
                continue

            if header == "INSIDE":
                key, value = [item.strip() for item in line.split(":")]
                if value.isdecimal():
                    value = int(value)
                attributes[key] = value
                continue

            if header == "AFTER":
                body.append(line)
                continue

        attributes["body"] = "\n".join(body)
        return attributes
