import pathlib

from jinja2 import BaseLoader, TemplateNotFound


class DocumentLoader(BaseLoader):
    def __init__(self, documents):
        self.documents = documents

    def get_source(self, environment, template):
        if template in self.documents:
            return (self.documents[template].body, None, None)
        else:
            raise TemplateNotFound(template)
