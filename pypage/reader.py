from markdown import Markdown

class Reader(object):
    pass

class MarkdownReader(Reader):

    def __init__(self):
        self.md = Markdown(extensions=['meta'])

    def read(self, filename):
        """
        Parse content and metadata of markdown files

        """
        metadatas = {}
        with open(filename) as f:
            content = self.md.convert(f.read())
            for key, value in self.md.Meta.items():
                metadatas[key.lower()] = value[0]

        return content, metadatas
